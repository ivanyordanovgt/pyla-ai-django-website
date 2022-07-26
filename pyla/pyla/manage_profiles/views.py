import random
import string
import django.views.generic as views
from django.contrib.auth import forms as auth_forms, get_user_model, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django import forms
from django.views.generic.edit import FormView
from django.core.mail import send_mail as email
from pyla import settings
from pyla.manage_profiles.forms import ProfileForm, CreateFeedbackForm, ForgotPasswordForm, ConfirmProfileForm
from pyla.manage_profiles.mixins import CRUDAccessMixin, FullCRUDProfileMixin
from pyla.manage_profiles.models import Profile, ContactUs, ChangePasswordKeys, AppUser, EmailKey

UserModel = get_user_model()

characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")


def generate_random_password():
    length = 20

    random.shuffle(characters)

    password = []
    for i in range(length):
        password.append(random.choice(characters))

    random.shuffle(password)

    return "".join(password)

# will only show the template if the user is logged in. Good for forum posts

class UserRegistrationForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'nickname',)

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(

            user=user,
        )

        if commit:
            profile.save()
        return user


class UserRegistrationView(views.CreateView):
    # form_class = auth_forms.UserCreationForm
    form_class = UserRegistrationForm
    template_name = 'manage_profiles/auth/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, *args, **kwargs):
        result = super().form_valid(*args, **kwargs)
        login(self.request, self.object)
        return result


class UserLoginView(auth_views.LoginView):
    template_name = 'manage_profiles/auth/login.html'

    def get_success_url(self):
        return reverse_lazy('index')


class UserLogoutView(auth_views.LogoutView):

    def get_next_page(self):
        return reverse_lazy('index')


class UserChangePasswordView(auth_views.PasswordChangeView):
    template_name = 'manage_profiles/auth/change_password.html'

    def get_success_url(self):
        return reverse_lazy('profile view',
                            kwargs={
                                'pk': self.request.user.profile.pk
                            })


class CustomResetPassword(auth_views.PasswordResetView):
    template_name = 'manage_profiles/auth/forgot-password.html'


class ForgotPasswordView(FormView):
    form_class = ForgotPasswordForm
    template_name = 'manage_profiles/auth/forgot-password.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        security_key = self.generate_security_key()
        ChangePasswordKeys.objects.create(email=form.get_email(), security_key=security_key)
        # form.send_email(email_subject='Thanks', message='Testing okay.')
        return super().form_valid(form)

    @staticmethod
    def generate_security_key():
        import random
        import array
        MAX_LEN = 12
        DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                             'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                             'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                             'z']

        UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                             'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                             'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                             'Z']

        SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
                   '*', '(', ')', '<']

        COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
        rand_digit = random.choice(DIGITS)
        rand_upper = random.choice(UPCASE_CHARACTERS)
        rand_lower = random.choice(LOCASE_CHARACTERS)
        rand_symbol = random.choice(SYMBOLS)
        temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
        for x in range(MAX_LEN - 4):
            temp_pass = temp_pass + random.choice(COMBINED_LIST)

            temp_pass_list = array.array('u', temp_pass)
            random.shuffle(temp_pass_list)
        password = ""
        for x in temp_pass_list:
            password = password + x
        return password


class FormView(ModelForm):
    class Meta:
        model = Profile
        fields = ('description', 'moto', 'profile_picture')


class ProfileView(LoginRequiredMixin, views.DetailView):
    template_name = 'manage_profiles/user/profile.html'
    model = Profile
    user = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.pk == self.kwargs['pk']:
            context['CRUD_ACCESS'] = True
            # if True instead of "Edit" button there will be "Add friend" button.
        return context


class ProfileEditView(LoginRequiredMixin, FullCRUDProfileMixin, views.UpdateView):  # TESTED
    template_name = 'manage_profiles/user/edit-profile.html'
    model = Profile
    form_class = ProfileForm

    def get_success_url(self):
        return reverse_lazy('index')


def send_email(request):
    return HttpResponse(f"Sent email")


class ConfirmProfileView(LoginRequiredMixin, views.FormView):
    form_class = ConfirmProfileForm
    template_name = 'manage_profiles/confirm-profile.html'

    def form_valid(self, form):
        key = form.cleaned_data['confirmationKey']
        
        try:
            keyDB = EmailKey.objects.filter(security_key=key)[0]
            if key == keyDB.security_key:
                user = AppUser.objects.get(pk=self.request.user.pk)
                user.is_activated = True
                user.save()

                userKeys = EmailKey.objects.filter(user_id=user.id)
                for key1 in userKeys:
                    key1.delete()

            return redirect('index')
        except:
            form.add_error('confirmationKey', 'The key you entered was invalid')
            return super(ConfirmProfileView, self).form_invalid(form)
class SentEmailView(LoginRequiredMixin, views.TemplateView):
    template_name = 'manage_profiles/confirmProfileBefore.html'


class RedirectToConfirmProfileView(LoginRequiredMixin, views.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        email = self.request.user.email
        email_subject = 'Confirm your email.'
        # sec_key = random.randint(10000, 99999999)
        sec_key = generate_random_password()
        message = f'The key to confirm your email is {sec_key}'
        from django.core.mail import send_mail
        user = AppUser.objects.get(pk=self.request.user.pk)
        key = EmailKey.objects.create(user=user, security_key=sec_key)
        key.save()

        send_mail(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email, ],
            fail_silently=False,
        )

        return reverse_lazy('send code and confirm')
