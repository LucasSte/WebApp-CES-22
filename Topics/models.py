from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class TopicInformation(models.Model):
    title_text = models.CharField(max_length=50)
    small_description = models.CharField(max_length=500)
    pub_date = models.DateField('date published')
    votes = models.IntegerField(default=0)
    big_description = models.CharField(max_length=10000)

    def __str__(self):
        return self.big_description


class Comment(models.Model):
    topic = models.ForeignKey(TopicInformation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.topic.title_text, str(self.user.username) )
