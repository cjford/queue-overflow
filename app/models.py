from django.conf import settings
from django.db import models
from django.db.models import Count, Sum
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
  def create_user(self, username, email, password):
    user = CustomUser(username = username, password = password)
    user.set_password(password)
    user.save()
    return user

class CustomUser(AbstractBaseUser):
  objects = CustomUserManager()
  username = models.CharField(max_length=20)
  first_name = models.CharField(max_length=50, blank=True)
  last_name = models.CharField(max_length=50, blank=True)
  email = models.EmailField(blank = False, unique=True)
  age = models.IntegerField(null=True, blank=True)
  location = models.CharField(max_length=50, blank=True)
  badges = models.ManyToManyField('Badge', related_name='badges', blank=True)
  active = models.BooleanField(default=False)
  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = 'email', 'password'

  def award_badges(self):
    Badge.objects.check_answer_guru(self)
    Badge.objects.check_discussion_leader(self)
    Badge.objects.check_veteran_asker(self)
    Badge.objects.check_veteran_answerer(self)
    Badge.objects.check_veteran_voter(self)


class QuestionManager(models.Manager):
  def top(self):
    return Question.objects.annotate(votes = Sum('qvote__vote')).order_by('-votes')

  def new(self):
    return Question.objects.all().order_by('-datetime')[:10]

  def active(self):
    return Question.objects.raw('SELECT DISTINCT question.id FROM (SELECT questions.a_datetime, questions.id FROM (SELECT app_question.id, app_answer.datetime as a_datetime FROM app_question, app_answer WHERE app_question.id = app_answer.question_id) as questions ORDER BY a_datetime DESC) as question')

  def unanswered(self):
    return Question.objects.annotate(answer_count = Count('answer')).filter(answer_count__lt = 1).order_by('-datetime')

class Question(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField()
  views = models.IntegerField(default=0)
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  datetime = models.DateTimeField(auto_now=True)
  tags = models.ManyToManyField('Tag', related_name='tags', blank=True)
  objects = QuestionManager()

  def username(self):
    return CustomUser.objects.get(id = self.user_id).username

  def votes(self):
    return self.qvote_set.all().aggregate(Sum('vote'))['vote__sum']

  def answer_count(self):
    return self.answer_set.count()


class Answer(models.Model):
  content = models.TextField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  question = models.ForeignKey(Question)
  datetime = models.DateTimeField(auto_now=True)

  def username(self):
    return CustomUser.objects.get(id = self.user_id).username

  def votes(self):
    return self.avote_set.all().aggregate(Sum('vote'))['vote__sum']


class BadgeManager(models.Manager):
  def check_answer_guru(self, user):
    count = 0
    for answer in user.answer_set.annotate(answer_count = Count('question__answer')).filter(answer_count__gte = 5).order_by('-avote'):
      if answer[0].user == user:
        count+=1
        if count == 5:
          badge = Badge.objects.get(name = 'Answer Guru')
          badge.save()
          badge.users.add(user)
          user.badges.add(badge)
          return

  def check_discussion_leader(self, user):
    if user.question_set.annotate(answer_count = Count('answer')).filter(answer_count__gte = 5).count() >= 5:
      badge = Badge.objects.get(name = 'Discussion Leader')
      badge.save()
      badge.users.add(user)
      user.badges.add(badge)
    
  def check_veteran_asker(self, user):
    if user.question_set.all().aggregate(Sum('qvote__vote'))['qvote__vote__sum'] >= 100:
      badge = Badge.objects.get(name = 'Veteran Asker')
      badge.save()
      badge.users.add(user)
      user.badges.add(badge)
    
  def check_veteran_answerer(self, user):
    if user.answer_set.all().aggregate(Sum('avote__vote'))['avote__vote__sum'] >= 100:
      badge = Badge.objects.get(name = 'Veteran Answerer')
      badge.save()
      badge.users.add(user)
      user.badges.add(badge)

  def check_veteran_voter(self, user):
    if user.avote_set.count() + user.qvote_set.count() >= 100:
      badge = Badge.objects.get(name = 'Veteran Voter')
      badge.save()
      badge.users.add(user)
      user.badges.add(badge)

class Badge(models.Model):
  name = models.CharField(max_length=50, unique='true')
  users = models.ManyToManyField('CustomUser', related_name='users', blank=True)
  description = models.CharField(max_length=200)
  objects = BadgeManager()


class QVote(models.Model):
  vote = models.IntegerField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  question = models.ForeignKey(Question)


class AVote(models.Model):
  vote = models.IntegerField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  answer = models.ForeignKey(Answer)


class Tag(models.Model):
  name = models.CharField(max_length=50, unique='true')
  questions = models.ManyToManyField('Question', related_name='questions')


class PasswordReset(models.Model):
  reset_id = models.CharField(max_length=40, unique='true')
  user = models.ForeignKey(CustomUser)
  datetime = models.DateTimeField(auto_now=True)


class UserActivation(models.Model):
  activate_id = models.CharField(max_length=40, unique='true')
  user = models.ForeignKey(CustomUser)
  datetime = models.DateTimeField(auto_now=True)
