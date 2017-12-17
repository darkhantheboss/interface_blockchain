from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.UserListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),
    url(
        regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),
    url(
        regex=r'^~smart_contract/$',
        view=views.ContractListView.as_view(),
        name='smart_contract'
    ),
    url(
        regex=r'^~smart_contract_detail/(?P<pk>[\w.@+-]+)/$',
        view=views.ContractUpdateView.as_view(),
        name='smart_contract_detail'
    ),
    url(
        regex=r'^~create_contract/$',
        view=views.ContractCreateView.as_view(),
        name='create_contract'
    ),
    url(
        regex=r'^~create_responsibility/(?P<pk>[\w.@+-]+)/$',
        view=views.ResponsibilityCreateView.as_view(),
        name='create_responsibility'
    ),
    url(
        regex=r'^~update_responsibility/(?P<pk>[\w.@+-]+)/$',
        view=views.ResponsibilityUpdateView.as_view(),
        name='update_responsibility'
    ),
]
