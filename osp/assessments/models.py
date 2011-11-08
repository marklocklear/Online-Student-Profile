from django.contrib.auth.models import User
from django.db import models

PERSONALITY_TYPE_CHOICES = (
    ('ENFP', 'Extraverted Intuitive Feeling Perceiving'),
    ('INFP', 'Introverted Intuitive Feeling Perceiving'),
    ('ENFJ', 'Extraverted Intuitive Feeling Judging'),
    ('INFJ', 'Introverted Intuitive Feeling Judging'),
    ('ESTJ', 'Extraverted Sensing Thinking Judging'),
    ('ISTJ', 'Introverted Sensing Thinking Judging'),
    ('ESFJ', 'Extraverted Sensing Feeling Judging'),
    ('ISFJ', 'Introverted Sensing Feeling Judging'),
    ('ENTP', 'Extraverted Intuitive Thinking Perceiving'),
    ('INTP', 'Introverted Intuitive Thinking Perceiving'),
    ('ENTJ', 'Extraverted Intuitive Thinking Judging'),
    ('INTJ', 'Introverted Intuitive Thinking Judging'),
    ('ESTP', 'Extraverted Sensing Thinking Perceiving'),
    ('ISTP', 'Introverted Sensing Thinking Perceiving'),
    ('ESFP', 'Extraverted Sensing Feeling Perceiving'),
    ('ISFP', 'Introverted Sensing Feeling Perceiving'),
)

class PersonalityTypeResult(models.Model):
    student = models.ForeignKey(User)
    answers = models.TextField()
    personality_type = models.CharField(max_length=4,
        choices=PERSONALITY_TYPE_CHOICES)
    first_category_score = models.IntegerField()
    second_category_score = models.IntegerField()
    third_category_score = models.IntegerField()
    fourth_category_score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)


class LearningStyleResult(models.Model):
    student = models.ForeignKey(User)
    answers = models.TextField()
    learning_style = models.CharField(max_length=255)
    kinesthetic_score = models.IntegerField()
    visual_score = models.IntegerField()
    auditory_score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)
