from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Personnalise le contenu du token JWT généré lors de la connexion.
    
    Hérite du serializer par défaut de SimpleJWT. Permet d'injecter 
    des informations supplémentaires de l'utilisateur (les "claims") 
    directement dans le payload du token (ex: nom, rôle, ID personnalisé).
    Ces informations seront ensuite décodables par le front-end.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Claims personnalisés
        # Exemple : token['name'] = user.name

        return token

# Sign up

class SignUpSerializer(serializers.ModelSerializer):
    """
    Gère la validation des données et la création d'un nouvel utilisateur.

    - Exige un email, un mot de passe (qui ne sera jamais retourné en lecture), 
      un prénom et un nom.
    - Vérifie que le mot de passe respecte les règles de sécurité de Django (`validate_password`).
    - Gère la création en base de données en s'assurant que le mot de passe 
      est correctement haché via la méthode `create_user` du modèle User.
    """
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('email', 'password','first_name', 'last_name')

    def create(self, validated_data):
        """
        Surcharge la méthode create par défaut pour utiliser `create_user` 
        (qui gère le hachage du mot de passe) et forcer l'utilisateur à être inactif.
        """
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=False, # User inactif par défaut en attente de validation (ex: email)
        )
        return user
    
# Password reset

class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Valide les données entrantes pour la demande de réinitialisation de mot de passe.
    
    S'assure uniquement que la requête contient une adresse email valide 
    et formattée correctement avant de laisser la vue faire sa recherche en base.
    """
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Valide le payload envoyé par le client (ex: React) lors de la 
    validation finale du nouveau mot de passe.
    
    Exige la présence des trois paramètres fondamentaux :
    - uidb64 : L'identifiant de l'utilisateur encodé.
    - token : Le jeton de sécurité cryptographique généré par Django.
    - password : Le nouveau mot de passe en clair (write_only).
    """
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)