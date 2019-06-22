from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from Topics.models import TopicInformation
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import UserLoginForm, UserRegistrationForm
from Topics.models import TopicInformation
from django.db.models import Q


def index(request):
    topics = TopicInformation.objects.order_by('-votes')
    query = request.GET.get('q')
    if query:
        topics = TopicInformation.objects.filter(
            Q(title_text__icontains=query) |
            Q(small_description__icontains=query) |
            Q(big_description__icontains=query)
        )
    context = {
        'topics':
            topics,
    }
    return render(request, 'WebApp/index.html', context)


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
    return render(request, 'WebApp/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('index')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'registration/register.html', context)
