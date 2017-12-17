from __future__ import unicode_literals

from django.db import models
from interface_blockchain.users.models import Responsibility
from django.utils.translation import ugettext_lazy as _


class Good(models.Model):
    name = models.CharField(_('Name of good'), blank=True, max_length=255)
    options = models.CharField(_('Options of good'), blank=True, max_length=255)
    description = models.CharField(_('Description of good'), blank=True, max_length=255)
    image = models.FileField(_('Description of good'), blank=True, null=True, upload_to='good/images/')
    tmp_responsibility = models.IntegerField(blank=True, null=True)
    tmp_amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Good, self).save(force_insert, force_update, using, update_fields)
        if self.tmp_responsibility and self.tmp_amount:
            Product.objects.create(responsibility_id=self.tmp_responsibility, amount=self.tmp_amount, good_id=self.id)


class Product(models.Model):
    good = models.ForeignKey(Good)
    amount = models.PositiveIntegerField(_('Name of goods'))
    responsibility = models.ForeignKey(Responsibility)

    def __str__(self):
        return self.good.name
