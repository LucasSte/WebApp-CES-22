from django.urls import path

from . import views

app_name = 'Topics'

urlpatterns = [
    path('<int:id>/post_edit', views.post_edit, name="post_edit"),
    path('<int:id>/', views.detail, name='detail'),
    path('<int:id>/upvote', views.upVote, name='upvote'),
    path('<int:id>/downvote', views.downVote, name='downvote'),
    path('new_entry', views.newEntry, name='new')
]
