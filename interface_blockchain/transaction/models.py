# coding=utf-8
from __future__ import unicode_literals
import requests
import json
from django.db import models
from interface_blockchain.users.models import Contract, User
from django.utils.translation import ugettext_lazy as _


class TransactionContract(models.Model):
    PROCESSING_STATUS, COMPLETED_STATUS, PARTIALLY_COMPLETED_STATUS, CANCELLED_STATUS = range(4)
    STATUSES_CONF = (
        (PROCESSING_STATUS, u'В процессе'),
        (COMPLETED_STATUS, u'Выполнен'),
        (PARTIALLY_COMPLETED_STATUS, u'Частично Выполнен'),
        (CANCELLED_STATUS, u'Отменен')
    )
    contract = models.ForeignKey(Contract)
    status = models.IntegerField(choices=STATUSES_CONF, default=PROCESSING_STATUS)
    create_date = models.DateTimeField(auto_now=True)
    completed_date = models.DateTimeField(blank=True, null=True)
    sender = models.ForeignKey(User, related_name='sender')
    receiver = models.ForeignKey(User, related_name='receiver')
    rating_customer = models.PositiveIntegerField(blank=True, null=True)
    rating_responsibilities = models.PositiveIntegerField(blank=True, null=True)
    review = models.TextField(max_length=255, blank=True, null=True)

    def get_full_rating(self):
        return self.rating_responsibilities / 10 * 0.7 + 0.3 * self.rating_customer / 10

    def get_status_display(self):
        return self.STATUSES_CONF[self.status][1]

    def __str__(self):
        return self.contract.name


class Payment(models.Model):
    PROCESSING_STATUS, COMPLETED_STATUS, ERROR_STATUS = range(3)
    STATUSES_CONF = (
        (PROCESSING_STATUS, u'В процессе'),
        (COMPLETED_STATUS, u'Выполнен'),
        (ERROR_STATUS, u'Ошибка')
    )
    transaction_payment = models.OneToOneField(TransactionContract)
    amount = models.PositiveIntegerField(_('Total charge'))
    status = models.IntegerField(choices=STATUSES_CONF, default=PROCESSING_STATUS)

    def get_status_display(self):
        return self.STATUSES_CONF[self.status][1]

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        data = {
            'sender': self.transaction_payment.sender.id,
            'recipient': self.transaction_payment.receiver.id,
            'rating': self.transaction_payment.get_full_rating(),
            'contract_id': self.transaction_payment.contract.id,
            'amount': self.amount,
        }
        if self.transaction_payment.contract.responsibility_set.all() and self.transaction_payment.contract.responsibility_set.values_list(
            'product', flat=True):
            data['product_id'] = self.transaction_payment.contract.responsibility_set.first().product_set.first().id
        else:
            data['product_id'] = 0
        requests.post('http://94.247.130.84/api/transactions/new', data=json.dumps(data))
        requests.get('http://94.247.130.84/api/mine')

        sender = self.transaction_payment.sender
        sender.balance -= self.amount
        sender.save()
        receiver = self.transaction_payment.receiver
        receiver.balance += self.amount
        receiver.save()
        super(Payment, self).save(*args, **kwargs)
