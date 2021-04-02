from django.urls import path
from .views import index, get_tags, get_entries

urlpatterns = [
    path('', index),
    path('api/tags', get_tags),
    path('api/entries', get_entries)
]