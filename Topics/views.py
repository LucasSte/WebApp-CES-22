from django.shortcuts import HttpResponseRedirect
from .models import *
from .forms import *
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.utils import timezone


def detail(request, id):
    try:
        topic = TopicInformation.objects.get(pk=id)
    except TopicInformation.DoesNotExist:
        raise Http404("Topic does not exist.")


    comments = Comment.objects.filter(topic=topic, reply=None).order_by('-id')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(topic=topic, user= request.user, content=content, reply=comment_qs)
            comment.save()
            #return HttpResponseRedirect(topic.get_abso lute_url())
    else:
        comment_form = CommentForm()


    context = {
        'topic': topic,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'Topics/detail.html', context)


def upvote(request, id):
    if request.user.is_authenticated:
        topic = get_object_or_404(TopicInformation, id=id)
        if topic.upvotes_users.filter(id=request.user.id).exists():
            topic.upvotes_users.remove(request.user)
            topic.votes = topic.votes - 1
        else:
            topic.upvotes_users.add(request.user)
            topic.votes = topic.votes + 1
            if topic.downvotes_users.filter(id=request.user.id).exists():
                topic.downvotes_users.remove(request.user)
                topic.votes = topic.votes + 1
        topic.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        messages.success(request, 'Login first to upVote')
        return HttpResponseRedirect(reverse('user_login'))

def downvote(request, id):
    if request.user.is_authenticated:
        topic = get_object_or_404(TopicInformation, id=id)
        if topic.downvotes_users.filter(id=request.user.id).exists():
            topic.downvotes_users.remove(request.user)
            topic.votes = topic.votes + 1
        else:
            topic.downvotes_users.add(request.user)
            topic.votes = topic.votes - 1
            if topic.upvotes_users.filter(id=request.user.id).exists():
                topic.upvotes_users.remove(request.user)
                topic.votes = topic.votes - 1
        topic.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.success(request, 'Login first to downVote')
        return HttpResponseRedirect(reverse('user_login'))


def newEntry(request):
    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('small_description') and request.POST.get('big_description'):
            new_topic = TopicInformation()
            new_topic.title_text = request.POST.get('title')
            new_topic.small_description = request.POST.get('small_description')
            new_topic.big_description = request.POST.get('big_description')
            new_topic.pub_date = timezone.now()
            new_topic.creator = request.user.get_username()
            new_topic.votes = 0
            new_topic.save()
            return render(request, 'Topics/detail.html', {'topic': new_topic})
        else:
            messages.success(request, 'Fill all the spaces, before submitting.')
            return render(request, 'Topics/new_entry.html')
    else:
        return render(request, 'Topics/new_entry.html')


def post_edit(request, id):
    topic = get_object_or_404(TopicInformation, id=id)
    if topic.creator != request.user.get_username():
        raise Http404()
    if request.method == 'POST':
        form = PostEditForm(request.POST or None, instance=topic)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(topic.get_absolute_url())
    else:
        form = PostEditForm(instance=topic)
    context = {
        'form': form,
        'topic': topic,
    }
    return render(request, 'WebApp/post_edit.html', context)
