# coding=utf-8
import requests
import json

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from datetime import datetime

from django.contrib import messages
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import TransactionContract, Payment
from .forms import TransactionContractForm
from interface_blockchain.users.models import Responsibility, Contract


class ChainListView(LoginRequiredMixin, TemplateView):
    template_name = 'transaction/chain_list.html'

    def get(self, request):
        ctx = {}
        r = requests.get('http://94.247.130.84/api/chain')
        return HttpResponse(json.dumps(r.json(), sort_keys=True, indent=4), content_type="application/json")


class DealListView(LoginRequiredMixin, ListView):
    model = TransactionContract
    template_name = 'transaction/deal_list.html'
    user = None

    def get(self, request, *args, **kwargs):
        self.user = request.user
        return super(DealListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(DealListView, self).get_queryset()
        return qs.filter(Q(sender=self.user) | Q(receiver=self.user))


class DealCreateView(LoginRequiredMixin, CreateView):
    template_name = 'transaction/deal_create.html'
    form_class = TransactionContractForm

    def get_context_data(self, request):
        return {
            'form': TransactionContractForm(initial={'sender': request.user})
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(request))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.object = form.save()
            return HttpResponseRedirect(reverse('transaction:deals'))
        else:
            messages.error(request, u'Произошла ошибка!')
            return super(DealCreateView, self).get(request, *args, **kwargs)


class DealDetailView(LoginRequiredMixin, TemplateView):
    model = TransactionContract
    template_name = 'transaction/deal_detail.html'
    user = None

    def get(self, request, *args, **kwargs):
        completed = request.GET.get('completed', None)
        self.user = request.user
        if completed:
            r = Responsibility.objects.get(id=int(completed))
            r.status = 1
            r.save()
        uncompleted = request.GET.get('uncompleted', None)
        if uncompleted:
            r = Responsibility.objects.get(id=int(uncompleted))
            r.status = 2
            r.save()
        self.object = TransactionContract.objects.get(id=int(kwargs['pk']))
        return super(DealDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = {}
        ctx['object'] = self.object
        ctx['responsibilities'] = self.object.contract.responsibility_set.all()
        ctx['may_check'] = self.object.sender != self.user
        ctx['may_finish'] = self.object.contract.responsibility_set.filter(status=0).count() == 0 and self.object.sender != self.user
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = TransactionContract.objects.get(id=int(kwargs['pk']))
        rating = int(request.POST.get('rating', None))
        comment = request.POST.get('comment', None)
        self.object.rating_customer = rating
        self.object.rating_responsibilities = self.object.contract.responsibility_set.filter(
            status=2).count() / self.object.contract.responsibility_set.count() * 10
        self.object.review = comment
        full_rating = (self.object.rating_responsibilities / 10 * 0.7) + 0.3 * rating / 10
        if full_rating == 1:
            self.object.status = 1
        else:
            self.object.status = 2
        self.object.completed_date = datetime.now()
        self.object.save()
        for r in self.object.contract.responsibility_set.all():
            r.status = 0
            r.save()
        transaction = Payment()
        transaction.transaction_payment = self.object
        transaction.amount = self.object.contract.total_amount * full_rating * 0.95
        transaction.save()
        contract = Contract()
        contract.total_amount = self.object.contract.total_amount * full_rating * 0.05
        contract.creator = self.object.sender
        contract.name = 'Comission'
        contract.save()
        transaction_comission = TransactionContract()
        transaction_comission.contract = contract
        transaction_comission.completed_date = datetime.now()
        transaction_comission.sender = self.object.sender
        transaction_comission.receiver = self.object.contract.creator
        transaction_comission.review = 'Comission'
        transaction_comission.rating_customer = 10
        transaction_comission.rating_responsibilities = 10
        transaction_comission.status = 1
        transaction_comission.save()
        comission_payment = Payment.objects.create(transaction_payment=transaction_comission,
                                                   amount=contract.total_amount)
        comission_payment.save()
        return HttpResponseRedirect(reverse('transaction:deals'))
