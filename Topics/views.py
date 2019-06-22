from django.shortcuts import HttpResponseRedirect
from .models import *
from .forms import *
from django.urls import reverse
from django.shortcuts import render
from django.http import Http404


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
    Topic = TopicInformation.objects.get(pk=id)
    Topic.votes += 1
    Topic.save()

    return HttpResponseRedirect(reverse('Topics:detail', args=[id]))


def downVote(request, id):
    Topic = TopicInformation.objects.get(pk=id)
    Topic.votes -= 1
    Topic.save()

    return HttpResponseRedirect(reverse('Topics:detail', args=[id]))



# Create your views here.
