from django import forms
from django.db import models
from django.contrib.auth import get_user_model
from app.models import Question, Answer, CustomUser, Tag

class LoginForm(forms.Form):
  username = forms.CharField(max_length=30, label="Username")
  password = forms.CharField(label="Password", widget=forms.PasswordInput())
  current_page = forms.CharField(required = False, widget=forms.HiddenInput())


class RegisterForm(forms.ModelForm):
  password = forms.CharField(label="Password", widget=forms.PasswordInput(render_value=False))
  confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(render_value=False))
  class Meta:
    model = get_user_model()
    fields = ('email', 'first_name', 'last_name', 'age', 'location', 'username', 'password') 

  def clean_confirm_password(self):
    password = self.cleaned_data.get("password")
    confirm_password = self.cleaned_data.get("confirm_password")
    if password and confirm_password and password != confirm_password:
      raise forms.ValidationError("Passwords don't match")
    return confirm_password
  

class EditUserForm(forms.Form):
  email = forms.EmailField(label="Email", required=False)
  first_name = forms.CharField(label="First name", required=False)
  last_name = forms.CharField(label="Last name", required=False)
  location = forms.CharField(label="Location", required=False)
  age = forms.IntegerField(label="Age", required=False)
  password = forms.CharField(label="Password", widget=forms.PasswordInput(render_value=False), required=False)
  confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(render_value=False), required=False)

  def clean_confirm_password(self):
    password = self.cleaned_data.get("password")
    confirm_password = self.cleaned_data.get("confirm_password")
    if (password != '' or confirm_password != '') and password != confirm_password:
      raise forms.ValidationError("Passwords don't match")
    return confirm_password


class AskForm(forms.ModelForm):
  tags = forms.CharField(max_length=100, label="Tags (comma separated list)")
  class Meta:
    model = Question
    fields = ('title', 'content')

class AnswerForm(forms.ModelForm):
  class Meta:
    model = Answer
    fields = ('content',)
