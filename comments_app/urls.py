from django.urls import path
from . import views

app_name = "comments_app"
urlpatterns = [
path('comment/article/<int:article_pk>/',views.article_comment,name="article_comment"),
]