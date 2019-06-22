from django.shortcuts import HttpResponseRedirect
from .models import TopicInformation
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
        Topic = TopicInformation.objects.get(pk=id)
    except TopicInformation.DoesNotExist:
        raise Http404("Topic does not exist.")

    return render(request, 'Topics/detail.html', {'Topic': Topic})


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
            return render(request, 'Topics/detail.html', {'Topic': new_topic})
        else:
            messages.success(request, 'Fill all the spaces, before submitting.')
            return render(request, 'Topics/new_entry.html')
    else:
        return render(request, 'Topics/new_entry.html')



# Create your views here.
