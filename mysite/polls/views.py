from django.http import HttpResponse, HttpResponseRedirect#, Http404
# from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views import generic
# from django.views.generic import View

# from .forms import UserForm
from .models import Question, Choice

from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """Return the last five published questions"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        # return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """Exclude any question that are not published"""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('polls/index.html')
#     #  need not write templates/polls/in.. as django is already set up to look in templates directory.
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
#     # return HttpResponse(template.render(context, request))
#
# # The render() function takes the request object as its first argument,
# # a template name as its second argument and a dictionary as its optional third argument.
# # It returns an HttpResponse object of the given template rendered with the given context
#
#
# def detail(request, question_id):
#     #try:
#     #    question = Question.objects.get(pk=question_id) # or id
#     #except:
#     #    raise Http404("Question doesn't exist.")
#     question = get_object_or_404(Question, pk=question_id)
#     # get_object_or_404 takes a Django model as first argument and an arbitrary no of keyword arguments, which it passes
#     # to get() function of the model's manager. It raises Http404 if object doesn't exist.
#     return render(request, 'polls/detail.html', {'question': question})
#     # return HttpResponse("You're looking at the question {}".format(question_id))
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question':question})
#
def vote(request, question_id):    # the code for our vote() has race condition
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question':question, 'error_message': "You didn't select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# class UserFormView(View):
#     form_class = UserForm
#     template_name = 'polls/registration_form.html'
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#
#         if form.is_valid():
#             user = form.save(commit=False)
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user.set_password(password)
#             user.save()
#
#             user = authenticate(username=username, password=password)
#
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('polls:index')
#
#         return render(request, self.template_name, {'form': form})

