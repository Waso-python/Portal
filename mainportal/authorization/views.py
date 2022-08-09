from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.contrib.auth.models import User
from usersProfile.models import ProfileUserModel
from .forms import *

class RegistrationPortal(View):
    template_name = 'authorization/registration.html'
    form = UserCreationForm()

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('interesting')
        return render(request, self.template_name, {'form':self.form})

    def post(self, request):
        if request.method == 'POST':
            self.form = UserCreationForm(request.POST)
            if self.form.is_valid():
                print(self.form.cleaned_data)
                self.form.save()
                user = authenticate(request,
                                    username=self.form.cleaned_data['username'],
                                    password=self.form.cleaned_data['password1']
                                    )
                if user is not None:
                    ProfileUserModel(user=User.objects.get(username=self.form.cleaned_data['username']), 
                                     keys={'places':'', 'law':'', 'type_proc':'', 'orgs':'', 'inn':'', 'subject':'', 'region':''}
                                    ).save()
                    login(request, user)
                return redirect('base')
            else:
                print('nope')
        return render(request, self.template_name, {'form':self.form})

class LoginPortal(View):
    template_name = 'authorization/login.html'
    form = LoginForm()

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('interesting')
        return render (request, self.template_name, {'form':self.form})

    def post(self, request):
        self.form = LoginForm(request.POST)
        if self.form.is_valid():
            print('is valid')
            user = authenticate(request,
                                username=self.form.cleaned_data['username'],
                                password=self.form.cleaned_data['password']
                                )
            if user is not None:
                login(request, user)
                return redirect('base')
        else:
            print('not valid')
        return render(request, self.template_name, {'form':self.form})
    

class LogoutPortal(View):

    def get(self, request):
        logout(request)
        return redirect('login')

