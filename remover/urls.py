from django.urls import path
from .views import index, remove_background, download_file

urlpatterns = [
    path('', index, name='index_page'),
    path('remove/', remove_background, name='remove_background'),
    path('download/', download_file, name='download_file'),
]
