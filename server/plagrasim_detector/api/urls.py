from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.file_upload, name='file-upload'),
    path('latest-file/', views.latest_file_detail, name='latest-file-detail'),  
    
]