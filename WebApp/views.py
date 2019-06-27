from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, HttpResponseRedirect, get_object_or_404
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
                form = UserLoginForm()
                context = {
                    'form': form,
                }
                messages.success(request, 'Wrong username or password')
                return render(request, 'WebApp/login.html', context)
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
