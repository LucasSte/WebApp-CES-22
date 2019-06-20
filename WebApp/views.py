from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from Topics.models import TopicInformation
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

def index(request):
    best_topic = TopicInformation.objects.order_by('-votes')
    context = {
        'best_voted_topics':
            best_topic,
    }
    return render(request, 'WebApp/index.html', context)


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'WebApp/signup.html'


def downvoteMain(request, id):
    Topic = TopicInformation.objects.get(pk=id)
    Topic.votes -= 1
    Topic.save()

    return HttpResponseRedirect(reverse('index'))


def upvoteMain(request, id):
    Topic = TopicInformation.objects.get(pk=id)
    Topic.votes += 1
    Topic.save()

    return HttpResponseRedirect(reverse('index'))
