from django.shortcuts import render, reverse, redirect
from users.forms import UserCreationForm, LoginForm, ResetForm
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from product.models import Files_upload
from py_decorators.decorators import check_owner
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView)
from Util import alfresco
import json


# Create your views here.

def index(request):
    context={}
    return render(request, 'index.html', context)


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            alfresco.createPerson(request.POST['full_name'], request.POST['email'], request.POST['password1'])
            form.save()
            messages.success(request, "Your account has been created successfully")
            return HttpResponseRedirect(reverse('index'))
    context = {'form': form, }
    return render(request, 'sensai/sign-up.html', context)

def login_view(request):
    form = LoginForm()
    password = ""
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            print('**************** password : ', password)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    response = HttpResponseRedirect(request.GET.get('next'))
                    user_id = json.loads(request.user.serialize())[0]['fields']['full_name']
                    request.session['usr'] = user_id
                    request.session['pwd'] = password
                    return response
                response = HttpResponseRedirect(reverse('dashboard'))
                user_id = json.loads(request.user.serialize())[0]['fields']['full_name']
                request.session['pwd'] = password
                request.session['usr'] = user_id
                return response
            else:
                messages.error(request, 'Incorrect Email or Password')
    context = {'form': form}
    return render(request, 'sensai/login.html', context)

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


class ResetPassword(PasswordResetView):
    template_name = 'sensai/password_reset.html'
    form_class = ResetForm


class ResetPasswordDone(PasswordResetDoneView):
    template_name = 'sensai/password_reset_done.html'

class ResetPasswordConfirm(PasswordResetConfirmView):
    template_name='sensai/password_reset_complete.html'
