from django.conf.urls import *
from .views import GoodListView, GoodCreateView

urlpatterns = [
    url(r'^goods/$', GoodListView.as_view(), name='goods'),
    url(r'^goods/create/(?P<pk>[\w.@+-]+)/$', GoodCreateView.as_view(), name='create_good'),
]
