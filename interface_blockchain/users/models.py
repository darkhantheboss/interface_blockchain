# coding=utf-8
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    balance = models.IntegerField(_('Balance of User'), default=0)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


@python_2_unicode_compatible
class Contract(models.Model):
    total_amount = models.PositiveIntegerField(_('Total amount of contract'))
    creator = models.ForeignKey(User)
    name = models.CharField(_('Name of Contract'), blank=True, max_length=255)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Responsibility(models.Model):
    PROCESSING_STATUS, COMPLETED_STATUS, UNCOMPLETED_STATUS = range(3)
    STATUSES_CONF = (
        (PROCESSING_STATUS, u'В процессе'),
        (COMPLETED_STATUS, u'Выполнен'),
        (UNCOMPLETED_STATUS, u'Не выполнен'),
    )
    contract = models.ForeignKey(Contract)
    name = models.CharField(_('Name of responsibility'), blank=True, max_length=255)
    status = models.IntegerField(choices=STATUSES_CONF, default=PROCESSING_STATUS)

    def get_status_display(self):
        return self.STATUSES_CONF[self.status][1]

    def __str__(self):
        return self.name
