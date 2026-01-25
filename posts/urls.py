from django.urls import path
from . import views
from .views import feed_view, post_create, toggle_like, tag_view

urlpatterns = [
    path('', feed_view, name='home'),
    path('post/new/', post_create, name='post_create'),
    path('post/like/<int:post_id>/', toggle_like, name='toggle_like'),
    path('tag/<str:tag_slug>/', tag_view, name='tag_filter'),
]