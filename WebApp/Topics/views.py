from django.shortcuts import HttpResponse
from .models import TopicInformation
from django.template import loader
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
        Topic = TopicInformation.objects.get(pk=id)
    except TopicInformation.DoesNotExist:
        raise Http404("Topic does not exist.")
    return render(request, 'Topics/detail.html', {'Topic': Topic})


# Create your views here.
