from app.models import CustomUser, AVote, QVote
from django import template
register = template.Library()

def current_vote(item, user_id):
    user = CustomUser.objects.get(id = user_id)
    if item.__class__.__name__ == 'Question':
        vote = QVote.objects.filter(question_id = item.id, user_id = user_id)
    elif item.__class__.__name__ == 'Answer':
        vote = AVote.objects.filter(answer_id = item.id, user = user_id)
    if vote.count() > 0:
        return vote[0].vote
    return None

current_vote = register.filter(current_vote)
