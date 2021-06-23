from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views import View

from .forms import CreateUserForm


class Registration(View):
    template_name = 'user/registration.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        create_user_form = CreateUserForm()
        context = {'create_user_form': create_user_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_create = CreateUserForm(request.POST, request.FILES)
        if user_create.is_valid():
            pass
        else:
            print(user_create.errors)
            if 'password2' in user_create.errors:
                errors = user_create.errors['password2']
                for error in errors:
                    messages.error(request, error)
            else:
                errors = 'Пока смотрю на разновидности ошибок'
                messages.error(request, errors)
            context = {'create_user_form': user_create}
            return render(request, self.template_name, context)
