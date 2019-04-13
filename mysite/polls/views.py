from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

"""
NOTE: this is functional way
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
    # NOTE: wrappe the data you want to sent to template as the third argument
"""


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions"""
        return Question.objects.order_by('-pub_date')[:5]


"""
NOTE: this functional way
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExists:
        raise Http404('Question does not exists')
    return render(request, 'polls/detail.html', {'question': question})
"""

"""
def detail(request, question_id):
    this is the same implementation as above
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
"""


class DetailView(generic.DeleteView):
    model = Question
    template_name = 'polls/detail.html'


"""
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
"""


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        # NOTE: request.POST['choice'] returns the ID of the selected choice, as a string. request.POST values are always strings.

    except (KeyError, Choice.DoesNotExist):
        # NOTE: request.POST['choice'] will raise KeyError if choice wasn’t provided in POST data. The above code checks for KeyError and redisplays the question form with an error message if choice isn’t given.

        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # NOTE: Always return an HttpResponseRedirect after successfully dealing with POST data. This prevents data from being posted twice if a user hits the Back button.

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # NOTE: reverse() helps avoid having to hardcode a URL in the view function. It is given the name of the view that we want to pass control to and the variable portion of the URL pattern that points to that view. In this case, using the URLconf we set up in Tutorial 3, this reverse() call will return a string like
