# coding=utf-8
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, CreateView

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from .models import User, Contract, Responsibility
from .forms import ContractForm, ResponsibilityForm


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class ContractListView(LoginRequiredMixin, ListView):
    model = Contract
    template_name = 'users/contract_list.html'
    user = None

    def get(self, request, *args, **kwargs):
        self.user = request.user
        return super(ContractListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Contract.objects.filter(creator=self.user)


class ContractUpdateView(LoginRequiredMixin, UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'users/update_contract.html'


class ContractCreateView(LoginRequiredMixin, CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'users/create_contract.html'

    def get_context_data(self, request):
        return {
            'form': ContractForm(initial={'creator': request.user.pk})
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(request))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, initial={'creator': request.user.pk})
        if form.is_valid():
            self.object = form.save()
            return HttpResponseRedirect(reverse('users:smart_contract_detail', args=[self.object.pk]))
        else:
            messages.error(request, u'Произошла ошибка!')
            return super(ContractCreateView, self).get(request, *args, **kwargs)


class ResponsibilityUpdateView(LoginRequiredMixin, UpdateView):
    model = Responsibility
    form_class = ResponsibilityForm
    template_name = 'users/update_responsibility.html'


class ResponsibilityCreateView(LoginRequiredMixin, CreateView):
    model = Responsibility
    form_class = ResponsibilityForm
    template_name = 'users/create_responsibility.html'
    contract_id = None

    def get_context_data(self, request):
        return {
            'form': ResponsibilityForm(initial={'contract': self.contract_id})
        }

    def get(self, request, *args, **kwargs):
        self.contract_id = kwargs['pk']
        return render(request, self.template_name, self.get_context_data(request))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.object = form.save()
            return HttpResponseRedirect(reverse('users:update_responsibility', args=[self.object.pk]))
        else:
            messages.error(request, u'Произошла ошибка!')
            return super(ResponsibilityCreateView, self).get(request, *args, **kwargs)
