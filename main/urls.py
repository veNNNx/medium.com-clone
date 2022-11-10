from django.urls import path
from django.contrib import admin
from django.urls import path, include # new
from . import views

urlpatterns = [
    path('', views.home),
    path('home', views.home),
    path('login', views.login),
    path('sign-up', views.sign_up),
    path('article/<int:id>', views.see_article),
    path('new-tags', views.new_tags),
    path('profile/<int:id>', views.profile),
    path('by_tag/<str:tag>', views.search_by_tag),
    path('delete/comment/', views.delete_comment),
    path('like/comment/', views.like_comment),
    path('dislike/comment/', views.dislike_comment),
]