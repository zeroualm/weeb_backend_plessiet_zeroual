from django.urls import path
from .views import SignUpView, RequestPasswordResetEmailView, PasswordResetConfirmView, LogoutView,CustomTokenView, CookieRefreshView

urlpatterns = [
    path('token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('password-reset/request/', RequestPasswordResetEmailView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
]