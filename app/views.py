from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from app.forms import LoginForm, RegisterForm 

def home(request):
  return render(request, 'home.html')

def login(request):
  if request.method == 'POST':
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
      user = authenticate(username = request.POST['username'], password = request.POST['password'])
      if user is not None:
        auth_login(request, user)
        messages.success(request, 'Successfully logged in')
        return HttpResponseRedirect(request.POST['current_page'])
      else:
        messages.error(request, 'Invalid login credentials.')
        return HttpResponseRedirect(request.POST['current_page'])
    else:
      messages.error(request, form.errors, extra_tags="safe")
      return HttpResponseRedirect(request.POST['current_page'])
  return HttpResponseRedirect('/#id_username')

def logout(request):
  auth_logout(request)
  messages.success(request, 'Successfully logged out')
  return HttpResponseRedirect(request.META['HTTP_REFERER'])

def register(request):
  if request.method == 'POST':
    register_form = RegisterForm(request.POST)
    if register_form.is_valid():
      register_form.save(request)
      return HttpResponseRedirect('/')
    else:
      return render(request, 'register.html', {'register_form':register_form})
  return render(request, 'register.html', {'register_form':RegisterForm})


