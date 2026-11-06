from django.urls import path

from .views import sentry_error

app_name = 'monitoring'

urlpatterns = [
    path('sentry-error/', sentry_error, name='sentry-error'),
]
