from django.conf import settings
from django.db import models
#from django.contrib.auth.models import User, UserManager
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
  def create_user(self, username, email, password):
    user = CustomUser(username = username, password = password)
    user.set_password(password)
    user.save()
    return user

class CustomUser(AbstractBaseUser):
  objects = CustomUserManager()
  username = models.CharField(max_length=100)
  first_name = models.CharField(max_length=100, blank=True)
  last_name = models.CharField(max_length=100, blank=True)
  email = models.EmailField(blank = False)
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = 'email', 'password'

class QuestionManager(models.Manager):
  def recent(self):
    return Question.objects.all().order_by('-datetime')[:10]
  
  def answers(self, question_id):
    return Answer.objects.all().filter(question_id = question_id).order_by('-datetime')

class Question(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField()
  views = models.IntegerField(default=0)
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  datetime = models.DateTimeField(auto_now = True)
  objects = QuestionManager()

  def __unicode__(self):
    return self.title

  def username(self):
    return CustomUser.objects.get(id = self.user_id).username

class Answer(models.Model):
  content = models.TextField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  question = models.ForeignKey(Question)
  datetime = models.DateTimeField(auto_now = True)

  def username(self):
    return CustomUser.objects.get(id = self.user_id).username

class Badge(models.Model):
  name = models.CharField(max_length=50, unique='true')
  description = models.CharField(max_length=200)

class EarnedBadge(models.Model):
  badge = models.ForeignKey(Badge)
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  datetime = models.DateTimeField(auto_now = True)

class QVote(models.Model):
  vote = models.IntegerField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  question = models.ForeignKey(Question)

class AVote(models.Model):
  vote = models.IntegerField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  answer = models.ForeignKey(Answer)

class QComment(models.Model):
  content = models.TextField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  question = models.ForeignKey(Question)
  datetime = models.DateTimeField(auto_now = True)

class AComment(models.Model):
  content = models.TextField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  answer = models.ForeignKey(Answer)
  datetime = models.DateTimeField(auto_now = True)
