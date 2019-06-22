from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from Topics.models import TopicInformation
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import UserLoginForm


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


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse('User is not active')
            else:
                return HttpResponse('Wrong user or password!')
    else:
        form = UserLoginForm()

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('index')
