from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm
from Topics.models import TopicInformation
from django.db.models import Q


def index(request):
    topics = TopicInformation.objects.order_by('-votes')

    if len(topics) < 5:
        first_page = False
        last_page = False
    else:
        first_page = True
        last_page = False

    topics = topics[0:5]
    query = request.GET.get('q')
    if query:
        search = True
        topics = TopicInformation.objects.filter(
            Q(title_text__icontains=query) |
            Q(small_description__icontains=query) |
            Q(big_description__icontains=query) |
            Q(creator__icontains=query)
        )
    else:
        search = False

    next_page = 2
    previous_page = -1

    context = {
        'topics':
            topics,
        'first_page': first_page,
        'last_page': last_page,
        'next_page': next_page,
        'previous_page': previous_page,
        'search': search,
    }


    return render(request, 'WebApp/index.html', context)

def loadPage(request, id):


    first_topic = (id-1)*5
    last_topic = 5*id
    topics = TopicInformation.objects.order_by('-votes')

    list_length = len(topics)

    if list_length <= last_topic:
        topics = topics[first_topic:]
        last_page = True
        first_page = False
    elif id == 1:
        topics = topics[first_topic:last_topic]
        first_page = True
        last_page = False
    else:
        topics = topics[first_topic:last_topic]
        first_page = False
        last_page = False

    next_page = id + 1
    previous_page = id - 1

    query = request.GET.get('q')
    if query:
        topics = TopicInformation.objects.filter(
            Q(title_text__icontains=query) |
            Q(small_description__icontains=query) |
            Q(big_description__icontains=query)
        )

    context = {
        'topics':
            topics, 'first_page': first_page, 'last_page': last_page,
        'next_page': next_page, 'previous_page': previous_page
    }

    return render(request, 'WebApp/index.html', context)


def downvoteMain(request, id):

    previous_url = request.META.get('HTTP_REFERER')

    if 'downvoted' + str(id) in request.COOKIES:
        value = request.COOKIES['downvoted'+ str(id)]
        if value == 'YES':
            messages.success(request, 'You have already downvoted that')
            #response = HttpResponseRedirect(reverse('index'))
            response = redirect(previous_url)
        elif value == 'PLUS':
            Topic = TopicInformation.objects.get(pk=id)
            Topic.votes -= 1
            Topic.save()
            #response = HttpResponseRedirect(reverse('index'))
            response = redirect(previous_url)
            response.set_cookie('downvoted' + str(id), 'NO')
            response.set_cookie('upvoted' + str(id), 'NO')
        else:
            Topic = TopicInformation.objects.get(pk=id)
            Topic.votes -= 1
            Topic.save()
            #response = HttpResponseRedirect(reverse('index'))
            response = redirect(previous_url)
            response.set_cookie('upvoted' + str(id), 'PLUS')
            response.set_cookie('downvoted' + str(id), 'YES')
    else:
        Topic = TopicInformation.objects.get(pk=id)
        Topic.votes -= 1
        Topic.save()
        response = redirect(previous_url)
        #response = HttpResponseRedirect(reverse('index'))
        response.set_cookie('downvoted' + str(id), 'YES')
        response.set_cookie('upvoted' + str(id), 'PLUS')

    return response


def upvoteMain(request, id):

    previous_url = request.META.get('HTTP_REFERER')

    if 'upvoted' + str(id) in request.COOKIES:
        value = request.COOKIES['upvoted' + str(id)]
        if value == 'YES':
            messages.success(request, 'You have already upvoted that')
            response = redirect(previous_url)
        elif value == 'PLUS':
            Topic = TopicInformation.objects.get(pk=id)
            Topic.votes += 1
            Topic.save()
            response = redirect(previous_url)
            response.set_cookie('upvoted' + str(id), 'NO')
            response.set_cookie('downvoted' + str(id), 'NO')
        else:
            Topic = TopicInformation.objects.get(pk=id)
            Topic.votes += 1
            Topic.save()
            response = redirect(previous_url)
            response.set_cookie('upvoted' + str(id), 'YES')
            response.set_cookie('downvoted' + str(id), 'PLUS')

    else:
        Topic = TopicInformation.objects.get(pk=id)
        Topic.votes += 1
        Topic.save()
        response = redirect(previous_url)
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
