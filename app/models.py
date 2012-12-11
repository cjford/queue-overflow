from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	views = models.IntegerField()
	user = models.ForeignKey(User)

class Answer(models.Model):
	content = models.TextField()
	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)

class Badge(models.Model):
	name = models.CharField(max_length=50, unique='true')
	description = models.CharField(max_length=200)

class EarnedBadge(models.Model):
	badge = models.ForeignKey(Badge)
	user = models.ForeignKey(User)
	date = models.DateTimeField()

class QVote(models.Model):
	vote = models.IntegerField()
	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)

class AVote(models.Model):
	vote = models.IntegerField()
	user = models.ForeignKey(User)
	answer = models.ForeignKey(Answer)

class QComment(models.Model):
	content = models.TextField()
	user = models.ForeignKey(User)
	question = models.ForeignKey(Question)

class AComment(models.Model):
	content = models.TextField()
	user = models.ForeignKey(User)
	answer = models.ForeignKey(Answer)
