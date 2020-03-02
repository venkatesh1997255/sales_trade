# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Sales(TimeStampModel):
    date = models.DateField(_('Date'), help_text="Date Mentioned")
    open = models.FloatField(_('Open Price'), help_text="Opening price quoted")
    high = models.FloatField(_('High Price'), help_text="High price quoted")
    low = models.FloatField(_('Low Price'), help_text="low price quoted")
    close = models.FloatField(_('Close Price'), help_text="closing price quoted")
    shares_traded = models.IntegerField(_('Share Traded'), help_text="shares traded mentioned")
    turnover = models.FloatField(_("Turn Over (Cr.)"), help_text="turn over quoted")

    def __str__(self):
        return "Sales: {}".format(self.pk)
