import random
from django.core.management.base import BaseCommand

from polls.factories import QuestionFactory, ChoiceFactory


class Command(BaseCommand):
    help = 'Generate test data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating new data...")

        for _ in range(10000):
            question = QuestionFactory()
            for _ in range(random.randint(2, 10)):
                ChoiceFactory(question=question)
