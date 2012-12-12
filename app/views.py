from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from app.forms import LoginForm, RegisterForm, AskForm, AnswerForm
from app.models import Question, Answer
from django.core.urlresolvers import reverse

def home(request):
  return render(request, 'home.html', {'recent_questions':Question.objects.recent()})

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

def ask(request):
  if request.method == "POST":
    ask_form = AskForm(request.POST)
    if ask_form.is_valid():
      question = Question(title = request.POST['title'], content = request.POST['content'], user_id = request.user.id)
      question.save()
      return HttpResponseRedirect(reverse('home'))
  return render(request, 'ask.html', {'ask_form':AskForm})


def answer(request):
  if request.method == "POST":
    answer_form = AnswerForm(request.POST)
    if answer_form.is_valid():
      answer = Answer(content = request.POST['content'], question_id = request.POST['question_id'], user_id = request.POST['user_id'])
      answer.save()
      return HttpResponseRedirect(reverse('home'))
  return HttpResponseRedirect(reverse('home'))
  
def question(request, question_id):
  return render(request, 'question.html', {'question':Question.objects.get(id=question_id), 'answer_form':AnswerForm, 'answers':Question.objects.answers(question_id)})

def user(request, user_id):
  user = User.objects.get(id=user_id)
  questions = user.question_set.all()
  answers = user.answer_set.all()
  return render(request, 'user.html', {'user':user, 'questions':questions, 'answers':answers})

def edit_user(request, user_id):
  return render(request, 'edit_user.html')
