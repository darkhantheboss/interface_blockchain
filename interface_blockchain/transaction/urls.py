from django.conf.urls import *
from .views import ChainListView, DealListView,DealCreateView, DealDetailView

urlpatterns = [
    url(r'^chains/$', ChainListView.as_view(), name='chains'),
    url(r'^deals/$', DealListView.as_view(), name='deals'),
    url(r'^deal/(?P<pk>[\w.@+-]+)/$', DealDetailView.as_view(), name='deal_detail'),
    url(r'^create_deal/$', DealCreateView.as_view(), name='create_deal'),
]
