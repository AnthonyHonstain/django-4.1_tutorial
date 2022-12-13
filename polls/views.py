import asyncio

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.utils import timezone

from .models import Question, Choice


# Create your views here.
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return render(request, 'polls/index.html', context)

async def detail(request, question_id):
    try:
        question = await Question.objects.filter(pub_date__lte=timezone.now()).aget(pk=question_id)
        choices = []
        async for choice in Choice.objects.select_related('question').filter(
                question_id=question_id, question__pub_date__lte=timezone.now()
        ).all():
            await asyncio.sleep(1)
            choices.append(choice)
        print('foo')

    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question, 'choices': choices })


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question':question})


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:25]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Exclude un-published questions"""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['choices'] = Choice.objects.select_related('question').filter(
            question_id=data['question'].id, question__pub_date__lte=timezone.now()
        ).all()
        return data


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """Exclude un-published questions"""
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "You didn't select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

