from django.shortcuts import HttpResponseRedirect
from .models import *
from .forms import *
from django.urls import reverse
from django.shortcuts import render
from django.http import Http404
from django.contrib import messages
from django.utils import timezone

def index(request):
    best_topic = TopicInformation.objects.order_by('votes')
    context = {
        'best_voted_topics':
            best_topic,
    }
    return render(request, 'Topics/index.html', context)


def detail(request, id):
    try:
        topic = TopicInformation.objects.get(pk=id)
    except TopicInformation.DoesNotExist:
        raise Http404("Topic does not exist.")

    comments = Comment.objects.filter(topic=topic).order_by('-id')

    if request.method == 'TOPIC':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            comment_form.save()
    else:
        comment_form = CommentForm()


    context = {
        'topic': topic,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'Topics/detail.html', context)


def upVote(request, id):
    if 'upvoted' + str(id) in request.COOKIES:
        value = request.COOKIES['upvoted' + str(id)]
        if value == 'YES':
            messages.success(request, 'You have already upvoted that')
            response = HttpResponseRedirect(reverse('Topics:detail', args=[id]))
        elif value == 'PLUS':
            Topic = TopicInformation.objects.get(pk=id)
            Topic.votes += 1
            Topic.save()
            response = HttpResponseRedirect(reverse('Topics:detail', args=[id]))
            response.set_cookie('upvoted' + str(id), 'NO')
        else:
            Topic = TopicInformation.objects.get(pk=id)
            Topic.votes += 1
            Topic.save()
            response = HttpResponseRedirect(reverse('Topics:detail', args=[id]))
            response.set_cookie('upvoted' + str(id), 'YES')
            response.set_cookie('downvoted' + str(id), 'PLUS')

    else:
        Topic = TopicInformation.objects.get(pk=id)
        Topic.votes += 1
        Topic.save()
        response = HttpResponseRedirect(reverse('Topics:detail', args=[id]))
        response.set_cookie('upvoted' + str(id), 'YES')
        response.set_cookie('downvoted' + str(id), 'PLUS')

    return response


def downVote(request, id):

    if 'downvoted' + str(id) in request.COOKIES:
        value = request.COOKIES['downvoted'+ str(id)]
        if value == 'YES':
            messages.success(request, 'You have already downvoted that')
            response = HttpResponseRedirect(reverse('Topics:detail', args=[id]))
        elif value == 'PLUS':
            Topic = TopicInformation.objects.get(pk=id)
            Topic.votes -= 1
            Topic.save()
            response = HttpResponseRedirect(reverse('Topics:detail', args=[id]))
            response.set_cookie('downvoted' + str(id), 'NO')
        else:
            Topic = TopicInformation.objects.get(pk=id)
            Topic.votes -= 1
            Topic.save()
            response = HttpResponseRedirect(reverse('Topics:detail', args=[id]))
            response.set_cookie('upvoted' + str(id), 'PLUS')
            response.set_cookie('downvoted' + str(id), 'YES')
    else:
        Topic = TopicInformation.objects.get(pk=id)
        Topic.votes -= 1
        Topic.save()
        response = HttpResponseRedirect(reverse('Topics:detail', args=[id]))
        response.set_cookie('downvoted' + str(id), 'YES')
        response.set_cookie('upvoted' + str(id), 'PLUS')

    return response


def newEntry(request):
    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('small_description') and request.POST.get('big_description'):
            new_topic = TopicInformation()
            new_topic.title_text = request.POST.get('title')
            new_topic.small_description = request.POST.get('small_description')
            new_topic.big_description = request.POST.get('big_description')
            new_topic.pub_date = timezone.now()
            new_topic.votes = 0
            new_topic.save()
            return render(request, 'Topics/detail.html', {'topic': new_topic})
        else:
            messages.success(request, 'Fill all the spaces, before submitting.')
            return render(request, 'Topics/new_entry.html')
    else:
        return render(request, 'Topics/new_entry.html')



# Create your views here.
