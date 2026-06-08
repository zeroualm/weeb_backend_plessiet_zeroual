from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .serializers import SignUpSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer

User = get_user_model() 

# -----------------------------
# Login view
# -----------------------------

class CustomTokenView(TokenObtainPairView):
    """
    Vue gérant la connexion d'un utilisateur.

    Elle surcharge le comportement par défaut de SimpleJWT pour placer 
    le jeton de rafraîchissement (refresh token) dans un cookie HttpOnly sécurisé,
    afin de le protéger contre les failles XSS côté client.
    """

    def post(self, request, *args, **kwargs):
        """
        Gère la requête POST pour authentifier un utilisateur.

        Args:
            request: L'objet requête DRF contenant les identifiants (email/mot de passe).
            *args, **kwargs: Arguments supplémentaires passés à la vue parent.

        Returns:
            Response: Un objet HTTP Response.
                - 200 OK: Contient uniquement l'access token (le refresh est placé en cookie).
                - 401 UNAUTHORIZED: Si les identifiants sont invalides.
        """
        # On laisse SimpleJWT valider les identifiants et générer les tokens
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get('refresh')
        
        if refresh_token:
            # Refresh token dans un cookie sécurisé
            response.set_cookie(
                key='refresh',
                value=refresh_token,
                httponly=True,
                secure=not settings.DEBUG, # True en production (HTTPS)
                samesite='Lax',
                max_age=3 * 60 # 3mins comme dans settings.py (SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])
            )
            # On retire le refresh token du JSON renvoyé au front
            del response.data['refresh'] 
            
        return response

class CookieRefreshView(TokenRefreshView):
    """
    Vue permettant le rafraîchissement de l'access token.

    Elle intercepte la requête pour lire le refresh token depuis le cookie
    HttpOnly du navigateur, le valide via SimpleJWT, et renvoie un nouvel
    access token ainsi qu'un nouveau cookie pour la rotation.
    """
    def post(self, request, *args, **kwargs):
        """
        Gère la requête POST pour rafraîchir la session.

        Args:
            request: L'objet requête DRF contenant les cookies du navigateur.
            *args, **kwargs: Arguments supplémentaires passés à la vue parent.

        Returns:
            Response: Un objet HTTP Response.
                - 200 OK: Contient le nouvel access token (et remplace le cookie refresh).
                - 401 UNAUTHORIZED: Si le token est invalide ou expiré.
        """
        # On récupère le token depuis le cookie
        refresh_token = request.COOKIES.get('refresh')
        
        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        new_refresh = response.data.get('refresh')
        if new_refresh:
            response.set_cookie(
                key='refresh',
                value=new_refresh,
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=3 * 60
            )
            del response.data['refresh']

        return response

# -----------------------------
# Logout view
# -----------------------------

class LogoutView(APIView):
    """
    Vue permettant à un utilisateur de se déconnecter.

    Cette vue est protégée par une authentification (IsAuthenticated). 
    Elle lit le refresh token dans le cookie, l'ajoute à la liste noire 
    pour l'invalider, puis supprime le cookie du navigateur.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Gère la requête POST pour la déconnexion.

        Args:
            request: L'objet requête DRF contenant le header d'authentification et les cookies.

        Returns:
            Response: Un objet HTTP Response indiquant que la déconnexion a réussi.
                - 205 RESET CONTENT: Déconnexion réussie.
        """
        refresh_token = request.COOKIES.get('refresh')
        
        if refresh_token:
            try:        
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                # Si le token est déjà expiré, on l'ignore
                pass 

        response = Response({"message": "Déconnexion réussie"}, status=status.HTTP_205_RESET_CONTENT)
        # On supprime le cookie du navigateur
        response.delete_cookie('refresh')
        return response

# -----------------------------
# SignUp view
# -----------------------------

class SignUpView(APIView):
    """
    Vue permettant l'inscription d'un nouvel utilisateur.

    Cet endpoint est public (AllowAny). Il accepte les données de 
    l'utilisateur, les valide via le SignUpSerializer, puis crée le compte.
    """
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer
    
    def post(self, request):
        """
        Gère la requête POST pour créer un utilisateur.

        Args:
            request: L'objet requête DRF contenant les données d'inscription (ex: email, mot de passe).

        Returns:
            Response: Un objet HTTP Response.
                - 201 CREATED: Si la création a réussi.
                - 400 BAD REQUEST: Si les données sont invalides (erreurs de validation du serializer).
        """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Utilisateur crée en attente de validation"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------
# Password reset views
# -----------------------------

class RequestPasswordResetEmailView(generics.GenericAPIView):
    """
    Vue permettant de demander la réinitialisation d'un mot de passe oublié.

    Cet endpoint vérifie si l'adresse email fournie correspond à un utilisateur 
    existant. Si c'est le cas, il génère un identifiant encodé (uidb64) et un 
    token cryptographique à usage unique, qui serviront à construire le lien 
    de réinitialisation.
    
    Note: Pour des raisons de sécurité, l'API renvoie toujours un succès (200 OK)
    afin d'éviter l'énumération des emails valides (Anti-Enumeration).
    """
    
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        """
        Gère la requête POST contenant l'email pour le reset.

        Args:
            request: L'objet requête DRF contenant l'email de l'utilisateur.

        Returns:
            Response: Un message générique de succès (200 OK), que l'email existe ou non.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()

        if user:
            # ID base64 "URL-safe"
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            # Token cryptographique
            token = PasswordResetTokenGenerator().make_token(user)

            # URL à faire dans le .env en prod
            reset_url = f"http://localhost:5173/reset-password?uidb64={uidb64}&token={token}"

            # Affichage terminal pour tests
            print(f"\n--- EMAIL DE REINITIALISATION ENVOYE A {user.email} ---")
            print(f"Token: {reset_url}")
            print(f"Token: {token}")
            print(f"UID (base64): {uidb64}")
            print("-------------------------------------------------------\n")

        # Réponse générique (opacité)
        return Response({"message": "Si un compte est associé à cet email, vous recevrez des instructions."},status=status.HTTP_200_OK)
    
class PasswordResetConfirmView(generics.GenericAPIView):

    """
    Vue permettant de confirmer le changement de mot de passe.

    Cet endpoint reçoit le nouveau mot de passe accompagné de l'identifiant 
    encodé (uidb64) et du token générés précédemment. Il valide l'authenticité 
    de la demande, vérifie que le token n'a pas expiré et n'a pas déjà été 
    utilisé, puis applique le nouveau mot de passe s'il respecte les critères 
    de sécurité de l'application.
    """

    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        """
        Gère la requête POST pour définir le nouveau mot de passe.

        Args:
            request: L'objet requête DRF contenant :
                - uidb64: L'ID de l'utilisateur encodé en base64.
                - token: Le token cryptographique de validation.
                - password: Le nouveau mot de passe choisi en clair.

        Returns:
            Response: Un objet HTTP Response.
                - 200 OK: Si le mot de passe a été modifié avec succès.
                - 400 BAD REQUEST: Si le token est invalide/expiré, si l'uidb64 est altéré, 
                                   ou si le nouveau mot de passe ne respecte pas les règles (ValidationError).
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data['uidb64']
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']

        try:
            # Décoder l'ID utilisateur reçu de React
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            # Vérifier la validité du token
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Le lien de réinitialisation est invalide ou a expiré.'},status=status.HTTP_400_BAD_REQUEST)

            # Valider le nouveau mot de passe contre les règles définies dans settings.py
            try:
                validate_password(password, user)
            except ValidationError as e:
                return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(password)
            user.save()

            return Response({'message': 'Le mot de passe a été réinitialisé avec succès.'}, status=status.HTTP_200_OK)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Lien de réinitialisation invalide.'}, status=status.HTTP_400_BAD_REQUEST)