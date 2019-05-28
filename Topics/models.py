from django.db import models

# Create your models here.


class TopicInformation(models.Model):
    title_text = models.CharField(max_length=50)
    small_description = models.CharField(max_length=500)
    pub_date = models.DateField('date published')
    votes = models.IntegerField(default=0)
    big_description = models.CharField(max_length=10000)

    def __str__(self):
        return self.big_description
