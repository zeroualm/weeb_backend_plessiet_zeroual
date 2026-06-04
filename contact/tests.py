from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ContactMessage


class ContactMessageCreateAPIViewTest(APITestCase):
    def test_contact_message_can_be_submitted(self):
        payload = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'phone_number': '0601020304',
            'message': 'Bonjour, je souhaite vous contacter.',
        }

        response = self.client.post(reverse('contact_submit'), payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            ContactMessage.objects.filter(
                email=payload['email'],
                phone_number=payload['phone_number'],
            ).exists()
        )
