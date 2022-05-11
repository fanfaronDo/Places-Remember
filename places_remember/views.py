import platform

import requests
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.views.generic import TemplateView
from social_django.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
from places_remember.forms import RememberForm
from places_remember.models import Remember


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
                return redirect('currentremember')

            except IntegrityError:
                return render(request, 'places_remember/signupuser.html', {'form': UserCreationForm(),
                                                                'error': 'Это имя пользователя уже занято'})

        else:
            # Tell the user the passwords didn't match
            return render(request, 'places_remember/signupuser.html', {'form': UserCreationForm(),
                                                            'error': 'Пароль не соответствует'})


def loginuser(request):
    if request.method == "GET":
        return render(request, 'places_remember/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'places_remember/loginuser.html', {'form': AuthenticationForm(),
                                                           'error': 'Имя или пароль не найдены'})
        else:
            login(request, user)
            return redirect('currentremember')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def home(request):
    return render(request, 'places_remember/home.html')


def currentremember(request):

    remember = Remember.objects.filter(user=request.user)
    return render(request, 'places_remember/currentremember.html', {'remember': remember})


def createremember(request):
    if request.GET == 'GET':
        return render(request, 'places_remember/createremember.html', {'form': RememberForm()})
    else:
        try:
            form = RememberForm(request.POST)
            newrem = form.save(commit=False)
            newrem.user = request.user
            newrem.save()
            return redirect('currentremember')
        except ValueError:
            return render(request, 'places_remember/createremember.html', {'form': RememberForm(),
                                                                         'error': 'Переданы неверные данные'})


def viewremember(request, rem_pk):
    remember = get_object_or_404(Remember, pk=rem_pk)
    if request.method == "GET":
        form = RememberForm(instance=remember)
        return render(request, 'places_remember/viewremember.html', {'remember': remember, 'form': form})
    else:
        try:
            form = RememberForm(request.POST, instance=remember)
            form.save()
            return redirect('currentremember')
        except ValueError:
            form = RememberForm(instance=remember)
            return render(request, 'places_remember/viewremember.html', {'remember': remember, 'form': form,
                                                                         'error': 'Ошибка'})





