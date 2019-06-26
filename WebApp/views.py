from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm
from Topics.models import TopicInformation
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    topics = TopicInformation.objects.order_by('-votes')
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

    page = request.GET.get('page', 1)
    paginator = Paginator(topics, 5)
    try:
        paginated_topics = paginator.page(page)
    except PageNotAnInteger:
        paginated_topics = paginator.page(1)
    except EmptyPage:
        paginated_topics = paginator.page(paginator.num_pages)

    if page is None:
        start_index = 0
        end_index = 5
    else:
        (start_index, end_index) = proper_pagination(paginated_topics, index=3)

    page_range = list(paginator.page_range)[start_index:end_index]

    if search:
        base_page_url = '?q=' + query + '&page='
    else:
        base_page_url = '?page='

    context = {
        'topics': paginated_topics,
        'base_page_url': base_page_url,
        'search': search,
        'page_range': page_range,
    }
    return render(request, 'WebApp/index.html', context)


def proper_pagination(posts, index):
    start_index = 0
    end_index = 5
    if posts.number > index:
        start_index = posts.number - index
        end_index = start_index + end_index
    return start_index, end_index


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
