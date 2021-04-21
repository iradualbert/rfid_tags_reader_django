from django.urls import path
from .views import index, get_tags, get_entries, get_bag_info, login

urlpatterns = [
    path('', index),
    path('api/login', login),
    path('api/bag-info', get_bag_info),
    path('api/tags', get_tags),
    path('api/entries', get_entries),
]