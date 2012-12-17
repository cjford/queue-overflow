from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.db.models import Sum
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context 
from django.conf import settings
from app.forms import *
from app.models import *
import hashlib, random, datetime


def home(request, sort='top'):
  if sort == 'top':
    questions = Question.objects.top()
  elif sort == 'new':
    questions = Question.objects.new()
  elif sort == 'active':
    questions = Question.objects.active()
  elif sort == 'unanswered':
    questions = Question.objects.unanswered()
  else:
    questions = Question.objects.all()
  return render(request, 'home.html', {'questions':questions, 'sort':sort})


def login(request):
  if request.method == 'POST':
    login_form = LoginForm(request.POST)

    if login_form.is_valid():
      user = authenticate(username = request.POST['username'], password = request.POST['password'])

      if user is not None:

        if user.active == False:
          messages.error(request, "This account is not activated. click <a href='%s'>Here</a> to request activation" % reverse('activate_user'))
          return HttpResponseRedirect(reverse('home'))
          
        auth_login(request, user)
        messages.success(request, 'Successfully logged in')
        return HttpResponseRedirect(request.POST['current_page'])

      else:
        messages.error(request, 'Invalid login credentials')
        return HttpResponseRedirect(request.POST['current_page'])

    else:
      messages.error(request, form.errors, extra_tags='safe')
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
      user = CustomUser.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
      user.email = request.POST['email']
      user.first_name = request.POST['first_name']
      user.last_name = request.POST['last_name']
      user.age = request.POST['age']
      user.location = request.POST['location']
      user.save()
      
      activate_id = hashlib.sha1(str(random.random())).hexdigest()
      ua = UserActivation(user_id = user.id, activate_id = activate_id)
      ua.save()
      url = 'http://' + settings.SITE_URL + reverse('activate_user', args=(str(activate_id),))

      plaintext = get_template('emails/activate_email.txt')
      htmltext = get_template('emails/activate_email.html')
      cxt = Context({'url':url, 'username':user.username})     

      msg = EmailMultiAlternatives('Account activation request', plaintext.render(cxt), 'from@example.com', [user.email])
      msg.attach_alternative(htmltext.render(cxt), 'text/html')
      msg.send()

      messages.success(request, 'Acitvation email sent')
      return HttpResponseRedirect('/')

    else:
      return render(request, 'register.html', {'register_form':register_form})

  return render(request, 'register.html', {'register_form':RegisterForm})


def activate_user(request, activate_id=None):
    if activate_id is not None:
      ua = UserActivation.objects.get(activate_id = activate_id)

      if request.method == 'POST':
        curr_time = datetime.datetime.utcnow().replace(tzinfo=None)
        expire_time = datetime.timedelta(hours=24)

        if (curr_time - ua.datetime.replace(tzinfo=None)) < expire_time:
          user = CustomUser.objects.get(id=ua.user_id)
          user.active = True
          user.save()
          ua.delete()
          user = authenticate(username = user.username, password = request.POST['password'])
          auth_login(request, user)
          messages.success(request, 'Account activated!')
          return HttpResponseRedirect(reverse('home'))
  
      return render(request, 'activate.html', {'activate_request':False})
      
    else:
      if request.method == 'POST':
        user = authenticate(username = request.POST['username'], password = request.POST['password'])

        if user is None:
          messages.error(request, 'Invalid login credentials')
          return HttpResponseRedirect(reverse('activate_user'))

        else:
          activate_id = hashlib.sha1(str(random.random())).hexdigest()
          ua = UserActivation(user_id = user.id, activate_id = activate_id)
          ua.save()
          url = 'http://' + settings.SITE_URL + reverse('activate_user', args=(str(activate_id),))

          plaintext = get_template('emails/activate_email.txt')
          htmltext = get_template('emails/activate_email.html')
          cxt = Context({'url':url, 'username':user.username})     

          msg = EmailMultiAlternatives('Account activation request', plaintext.render(cxt), 'from@example.com', [user.email])
          msg.attach_alternative(htmltext.render(cxt), 'text/html')
          msg.send()
          messages.success(request, 'Activation email sent')
        return HttpResponseRedirect(reverse('home'))

      return render(request, 'activate.html', {'activate_request':True})


def deactivate_user(request, user_id):
  if request.user.is_authenticated and int(request.user.id) == int(user_id):
    user = CustomUser.objects.get(id=user_id)
    user.active = False
    auth_logout(request)
    user.save()
    messages.success(request, 'Account deactivated')

  return HttpResponseRedirect(reverse('home'))


def ask(request):
  if request.method == 'POST':
    ask_form = AskForm(request.POST)

    if ask_form.is_valid():
      question = Question(title = request.POST['title'], content = request.POST['content'], user_id = request.user.id)
      question.save()

      # Initialize vote sum to 0 to avoid 'Votes: None'
      initializer = CustomUser.objects.get(username='vote_initializer')
      vote = QVote(question = question, user=initializer, vote = 0)
      vote.save()

      tags = request.POST['tags'].split(',')
      for tag in tags:
        tag = tag.strip()
        tag = tag.capitalize()

        if Tag.objects.filter(name=tag).count() <= 0:
          new_tag = Tag(name = tag)
          new_tag.save()
          new_tag.questions.add(question.id)
          question.tags.add(new_tag.id)

      return HttpResponseRedirect(reverse('question', args=(question.id,)))

  return render(request, 'ask.html', {'ask_form':AskForm})


def answer(request):
  if request.method == 'POST':
    answer_form = AnswerForm(request.POST)

    if answer_form.is_valid():
      answer = Answer(content = request.POST['content'], question_id = request.POST['question_id'], user_id = request.POST['user_id'])
      answer.save()

      # Initialize vote sum to 0 to avoid 'Votes: None'
      initializer = CustomUser.objects.get(username='vote_initializer')
      vote = AVote(answer = answer, user=initializer, vote = 0)
      vote.save()

      return HttpResponseRedirect(reverse('question', args=(answer.question_id,)))

  return HttpResponseRedirect(reverse('home'))
  
def question(request, question_id):
  question = Question.objects.get(id=question_id)
  answers = Answer.objects.filter(question=question).annotate(vote_count=Sum('avote__vote')).order_by('-vote_count')
  return render(request, 'question.html', {'question':question, 'answer_form':AnswerForm, 'answers':answers})


def edit_question(request, question_id):
  if request.method == 'POST':
    question = Question.objects.get(id=question_id)
    question.title = request.POST['title']
    question.content = request.POST['content']
    question.save()

    tags = request.POST['tags'].split(',')
    for tag in tags:
      tag = tag.strip()
      tag = tag.capitalize()

      if Tag.objects.filter(name=tag).count() <= 0:
        new_tag = Tag(name = tag)
        new_tag.save()
        new_tag.questions.add(question.id)
        question.tags.add(new_tag.id)

    return HttpResponseRedirect(reverse('question', args=(question_id,)))

  else:
    if request.user.id != Question.objects.get(id=question_id).user_id:
      return HttpReponseRedirect(reverse('home'))
    else:
      question_data = Question.objects.get(id=question_id)
      return render(request, 'edit_question.html', {'ask_form':AskForm(instance=question_data)})


def user(request, user_id):
  user = CustomUser.objects.get(id=user_id)
  user.award_badges()

  if not user.active:
    response = HttpResponse('This account is no longer available')
    response.status_code=410
    return response

  else:
    questions = user.question_set.all()
    answers = user.answer_set.all()
    return render(request, 'user.html', {'profile_owner':user, 'questions':questions, 'answers':answers})


def edit_user(request, user_id):
  if request.method == 'POST':
    edit_form = EditUserForm(request.POST)

    if edit_form.is_valid():
      user = CustomUser.objects.get(id = request.user.id)

      for key in edit_form.cleaned_data.keys():
        if edit_form.cleaned_data[key] != '' and edit_form.cleaned_data[key] is not None:
          if key == 'password':
            user.set_password(edit_form.cleaned_data['password'])
          else:
            setattr(user, key, edit_form.cleaned_data[key])
      user.save()

      return HttpResponseRedirect(reverse('user', args=(user_id,)))
    else:
      return render(request, 'edit_user.html', {'edit_form':edit_form})

  if request.user.is_authenticated and int(request.user.id) == int(user_id):
    return render(request, 'edit_user.html', {'edit_form':EditUserForm})
  else:
    return HttpResponseRedirect(reverse('home'))


def vote(request):
  if request.method == 'POST':

    if int(request.POST['item_type']) == 1:
      try:
        vote = QVote.objects.get(user_id=request.user.id, question_id = request.POST['item_id'])
      except QVote.DoesNotExist:
        vote = QVote()

      vote.vote = request.POST['vote']
      vote.question_id = request.POST['item_id']
      vote.user_id = request.user.id
      vote.save()

    elif int(request.POST['item_type']) == 2:
      try:
        vote = AVote.objects.get(user_id=request.user.id, answer_id = request.POST['item_id'])
      except AVote.DoesNotExist:
        vote = AVote()

      vote.vote = request.POST['vote']
      vote.answer_id = request.POST['item_id']
      vote.user_id = request.user.id
      vote.save()

  return HttpResponseRedirect(request.POST['current_page'])


def tags(request):
  return render(request, 'tags.html', {'tags':Tag.objects.all().order_by('name')})

def tag(request, tag_id):
  return render(request, 'tag.html', {'tag':Tag.objects.get(id=tag_id), 'questions':Question.objects.filter(tags__in=[tag_id])})


def badges(request):
  return render(request, 'badges.html', {'badges':Badge.objects.all().order_by('name')})

def badge(request, badge_id):
  return render(request, 'badge.html', {'badge':Badge.objects.get(id=badge_id), 'users':CustomUser.objects.filter(badges__in=[badge_id])})


def reset_password(request, reset_id=None):
  if reset_id is not None:
    pr = PasswordReset.objects.get(reset_id=reset_id)
    curr_time = datetime.datetime.utcnow().replace(tzinfo=None)
    expire_time = datetime.timedelta(hours=24)

    if (curr_time - pr.datetime.replace(tzinfo=None)) < expire_time:
      new_password = hashlib.sha1(str(random.random())).hexdigest()[:10]
      user = CustomUser.objects.get(id=pr.user_id)
      user.set_password(new_password)
      user.save()
      pr.delete()

      url = 'http://' + settings.SITE_URL + reverse('home')
      plaintext = get_template('emails/reset_email.txt')
      htmltext = get_template('emails/reset_email.html')
      cxt = Context({'home_url':url, 'username':user.username, 'new_password':new_password})     

      msg = EmailMultiAlternatives('Your password has been reset', plaintext.render(cxt), '', [user.email])
      msg.attach_alternative(htmltext.render(cxt), 'text/html')
      msg.send()

      messages.success(request, 'New password email sent')
      return HttpResponseRedirect(reverse('home'))

  if request.method == 'POST':
    try: 
      user = CustomUser.objects.get(username=request.POST['name_or_email'])
      email = user.email
    except CustomUser.DoesNotExist:
      try: 
        email = request.POST['name_or_email']
        user = CustomUser.objects.get(email=email)
      except CustomUser.DoesNotExist:
        messages.error(request, 'No user with that username or email found')
        return HttpResponseRedirect(reverse('reset_password'))

    reset_id = hashlib.sha1(str(random.random())).hexdigest()
    pr = PasswordReset(reset_id = reset_id, user_id = user.id) 
    pr.save()
    url = 'http://' + settings.SITE_URL + reverse('reset_password', args=(str(reset_id),))

    plaintext = get_template('emails/request_email.txt')
    htmltext = get_template('emails/request_email.html')
    cxt = Context({'url':url, 'username':user.username})     

    msg = EmailMultiAlternatives('Password reset request', plaintext.render(cxt), '', [email])
    msg.attach_alternative(htmltext.render(cxt), 'text/html')
    msg.send()

    messages.success(request, 'Reset email sent')
    return HttpResponseRedirect(reverse('reset_password'))

  return render(request, 'reset_password.html')
