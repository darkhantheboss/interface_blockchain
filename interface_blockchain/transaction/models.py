# coding=utf-8
from __future__ import unicode_literals

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
    rating_customer = models.PositiveIntegerField()
    rating_responsibilities = models.PositiveIntegerField()
    review = models.TextField(max_length=255, blank=True, null=True)

    def get_status_display(self):
        return self.STATUSES_CONF[self.status]

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
        return self.STATUSES_CONF[self.status]

    def __str__(self):
        return self.id
