from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from pyla.manage_profiles.views import UserRegistrationView, UserLoginView, UserLogoutView, ProfileView, send_email, \
    ConfirmProfileView, SentEmailView, RedirectToConfirmProfileView
from pyla.manage_profiles.views import ProfileEditView, UserChangePasswordView, ForgotPasswordView, CustomResetPassword

urlpatterns = [

    path('register/', UserRegistrationView.as_view(), name='register user'),
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout', UserLogoutView.as_view(), name='logout user'),
    path('change-password/,', UserChangePasswordView.as_view(), name='change password'),
    path('completed-registraion/', TemplateView.as_view(template_name="manage_profiles/auth/successful_register.html"),
         name='registered successfully'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile view'),
    path('edit-profile/<int:pk>', ProfileEditView.as_view(), name='edit profile'),
    path('sent-email/', CustomResetPassword.as_view(), name='send email'),
    #################################################################################
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reset/done/', ConfirmProfileView.as_view(), name='confirm account'),
    path('confirm-email/', SentEmailView.as_view(), name='email confirmation'),
    path('confirm-email/code/', ConfirmProfileView.as_view(), name='send code and confirm'),
    path('confirm-email/code/redirect', RedirectToConfirmProfileView.as_view(), name='send email and redirect'),

]
