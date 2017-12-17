# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import ListView, CreateView
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from .models import Good
from .forms import GoodForm

from django.contrib.auth.mixins import LoginRequiredMixin


class GoodListView(LoginRequiredMixin, ListView):
    model = Good
    template_name = 'product/goods.html'
    user = None

    def get(self, request, *args, **kwargs):
        self.user = request.user
        return super(GoodListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Good.objects.all()


class GoodCreateView(LoginRequiredMixin, CreateView):
    model = Good
    form_class = GoodForm
    template_name = 'product/create_good.html'
    responsibility = None

    def get_context_data(self, request):
        return {
            'form': GoodForm(initial={'tmp_responsibility': self.responsibility})
        }

    def get(self, request, *args, **kwargs):
        self.responsibility = kwargs['pk']
        return render(request, self.template_name, self.get_context_data(request))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save()
            return HttpResponseRedirect(reverse('users:smart_contract'))
        else:
            messages.error(request, u'Произошла ошибка!')
            return super(GoodCreateView, self).get(request, *args, **kwargs)
