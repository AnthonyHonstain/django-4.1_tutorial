import factory
from factory.django import DjangoModelFactory
from django.utils import timezone

from .models import Question, Choice


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question

    question_text = factory.Faker('sentence')
    pub_date = factory.Faker('date_time', tzinfo=timezone.timezone.utc)


class ChoiceFactory(DjangoModelFactory):
    class Meta:
        model = Choice

    question = factory.SubFactory(QuestionFactory)
    choice_text = factory.Faker('sentence')
    votes = factory.Faker('random_int')
