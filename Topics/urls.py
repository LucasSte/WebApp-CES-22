from django.urls import path

from . import views

app_name = 'Topics'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.detail, name='detail'),
    path('<int:id>/upvote', views.upVote, name='upvote'),
    path('<int:id>/downvote', views.downVote, name='downvote')
]
