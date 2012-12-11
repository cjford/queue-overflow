from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

class LoginForm(forms.Form):
  username = forms.CharField(max_length=30, label="Username")
  password = forms.CharField(label="Password", widget=forms.PasswordInput())
  current_page = forms.CharField(required = False, widget=forms.HiddenInput())

class RegisterForm(forms.ModelForm):
  email = forms.EmailField(label="Email")
  first_name = forms.CharField(max_length=30, label="First name", required=False)
  last_name = forms.CharField(max_length=30, label="Last name", required=False)
  username = forms.CharField(max_length=30, label="Username")
  password = forms.CharField(label="Password", widget=forms.PasswordInput(render_value=False))
  confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(render_value=False))
  class Meta:
    model = User
    fields = ('email', 'first_name', 'last_name', 'username', 'password') 

  def clean_confirm_password(self):
    password = self.cleaned_data.get("password")
    confirm_password = self.cleaned_data.get("confirm_password")
    if password and confirm_password and password != confirm_password:
        raise forms.ValidationError("Passwords don't match")
    return confirm_password
  
  def save(self, request):
    user = User.objects.create_user(self.cleaned_data['username'], self.cleaned_data['email'], self.cleaned_data['password'])
    user.save()
    user = authenticate(username = self.cleaned_data['username'], password = self.cleaned_data['password'])
    login(request, user)
