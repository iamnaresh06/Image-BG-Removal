from django.urls import path
from .views import index, remove_background

urlpatterns = [
    path('', index, name='index_page'),
    path('remove/', remove_background, name='remove_background'),
]
