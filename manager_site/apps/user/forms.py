from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'patronymic',
            'gender',
            'phone',
            'photo',
            'password1',
            'password2',
        ]


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = [
            'email',
            'password1',
        ]
