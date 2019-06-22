from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from Topics.models import TopicInformation
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm


def index(request):
    best_topic = TopicInformation.objects.order_by('-votes')
    context = {
        'best_voted_topics':
            best_topic,
    }
    return render(request, 'WebApp/index.html', context)


def downvoteMain(request, id):

    if 'downvoted' + str(id) in request.COOKIES:
        value = request.COOKIES['downvoted'+ str(id)]
        if value == 'YES':
            messages.success(request, 'You have already downvoted that')
            response = HttpResponseRedirect(reverse('index'))
        elif value == 'PLUS':
            Topic = TopicInformation.objects.get(pk=id)
            Topic.votes -= 1
            Topic.save()
            response = HttpResponseRedirect(reverse('index'))
            response.set_cookie('downvoted' + str(id), 'NO')
        else:
            Topic = TopicInformation.objects.get(pk=id)
            Topic.votes -= 1
            Topic.save()
            response = HttpResponseRedirect(reverse('index'))
            response.set_cookie('upvoted' + str(id), 'PLUS')
            response.set_cookie('downvoted' + str(id), 'YES')
    else:
        Topic = TopicInformation.objects.get(pk=id)
        Topic.votes -= 1
        Topic.save()
        response = HttpResponseRedirect(reverse('index'))
        response.set_cookie('downvoted' + str(id), 'YES')
        response.set_cookie('upvoted' + str(id), 'PLUS')

    return response


def upvoteMain(request, id):
    if 'upvoted' + str(id) in request.COOKIES:
        value = request.COOKIES['upvoted' + str(id)]
        if value == 'YES':
            messages.success(request, 'You have already upvoted that')
            response = HttpResponseRedirect(reverse('index'))
        elif value == 'PLUS':
            Topic = TopicInformation.objects.get(pk=id)
            Topic.votes += 1
            Topic.save()
            response = HttpResponseRedirect(reverse('index'))
            response.set_cookie('upvoted' + str(id), 'NO')
        else:
            Topic = TopicInformation.objects.get(pk=id)
            Topic.votes += 1
            Topic.save()
            response = HttpResponseRedirect(reverse('index'))
            response.set_cookie('upvoted' + str(id), 'YES')
            response.set_cookie('downvoted' + str(id), 'PLUS')

    else:
        Topic = TopicInformation.objects.get(pk=id)
        Topic.votes += 1
        Topic.save()
        response = HttpResponseRedirect(reverse('index'))
        response.set_cookie('upvoted' + str(id), 'YES')
        response.set_cookie('downvoted' + str(id), 'PLUS')
    return response


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
