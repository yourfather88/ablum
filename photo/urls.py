from django.urls import path, include
from photo.views import home, upload, oss_home

app_name = 'photo'

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload, name='upload'),
    path('oss_home', oss_home, name='oss_home'),

]
