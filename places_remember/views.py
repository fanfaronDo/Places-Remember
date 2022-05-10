from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.views.generic import TemplateView
from social_django.models import UserSocialAuth


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "places_remember/home.html"

def signupuser(request):
    if request.method == "GET":
        return render(request, 'places_remember/signupuser.html', {'form': UserCreationForm()})
    else:
        # Creat a new user
        #print(request.POST['password1'])

        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('userrecords')

            except IntegrityError:
                return render(request, 'places_remember/signupuser.html', {'form': UserCreationForm(),
                                                                'error': 'That username has already been taken'})

        else:
            # Tell the user the passwords didn't match
            return render(request, 'places_remember/signupuser.html', {'form': UserCreationForm(),
                                                            'error': 'Password did not match'})


def loginuser(request):
    if request.method == "GET":
        return render(request, 'places_remember/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'places_remember/loginuser.html', {'form': AuthenticationForm(),
                                                           'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('userrecords')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def userrecords(request):
    return render(request, 'places_remember/userrecords.html')


def home(request):
    return render(request, 'places_remember/home.html')