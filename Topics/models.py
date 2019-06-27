from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class TopicInformation(models.Model):
    title_text = models.CharField(max_length=50, default="")
    small_description = models.TextField(max_length=500)
    pub_date = models.DateField('date published')
    votes = models.IntegerField(default=0)
    upvotes_users = models.ManyToManyField(User, related_name="upvotes_users", blank=True)
    downvotes_users = models.ManyToManyField(User, related_name="downvotes_users", blank=True)
    big_description = models.TextField(max_length=10000)
    creator = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.big_description

    def get_absolute_url(self):
        return reverse("Topics:detail", args=[self.id])


class Comment(models.Model):
    topic = models.ForeignKey(TopicInformation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', null=True, related_name="replies", on_delete=models.CASCADE)
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.topic.title_text, str(self.user.username) )
