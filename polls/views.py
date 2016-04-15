from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import *


def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return render(request, 'polls/login.html')

def register(request):
    if request.method == 'POST':
        uf = UserCreateForm(request.POST, prefix='user')
        if uf.is_valid() :
            user = uf.save()
            return HttpResponseRedirect("/")
    else:
        uf = UserCreateForm(prefix='user')
    return render(request, 'polls/register.html',{'userform':uf}) #,  userprofileform=upf),

#@login_required(login_url='login/')

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the user polls
        """
        if self.request.user.is_authenticated():
            return Question.objects.filter(
                user= self.request.user
            ).order_by('-pub_date')
        else:
            return []

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def createQuestion(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request=request)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = QuestionForm()

    return render(request, 'polls/new_question.html',{'form':form})

class QuestionChoiceList(generic.ListView):
    model = Question
    template_name = 'polls/choices.html'

    #def get_queryset(self):
    #    self.question = get_object_or_404(Question, name=self.args[0])
    #    return Choice.objects.filter(publisher=self.publisher)
