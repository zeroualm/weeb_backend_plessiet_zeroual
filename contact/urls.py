from django.urls import path

from .views import ContactMessageCreateAPIView


urlpatterns = [
    path('', ContactMessageCreateAPIView.as_view(), name='contact_submit'),
]
