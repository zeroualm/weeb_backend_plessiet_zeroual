from rest_framework import serializers

from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    """
    Serialiseur pour enregistrer les messages de contact.
    """

    class Meta:
        model = ContactMessage
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'message',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
