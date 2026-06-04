from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsActiveUserOrReadOnly(BasePermission):
    """
    Autorise la lecture publique et reserve l'ecriture aux utilisateurs actifs.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
        )
