from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home$', views.home, name='home'),
    url(r'^destination/(?P<travelplan_id>\d+)$', views.goToDestination, name='destination'),
    url(r'^add$', views.add, name='add'),
    url(r'^addplan/(?P<user_id>\d+)$', views.addplan, name='addplan'),
    url(r'^join/(?P<travelplan_id>\d+)$', views.join, name='join'),
]
