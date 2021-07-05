from django.urls import path
from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^start', views.start),
    url(r'^questions_([A-z0-9]{1,10})',views.questions),
    url(r'^result',views.result)
]

