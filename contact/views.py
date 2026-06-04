from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactMessageCreateAPIView(generics.CreateAPIView):
    """
    Vue pour soumettre un message depuis le formulaire de contact.
    """

    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
