# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class MailLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=200, verbose_name='Статус')
    email = models.EmailField(verbose_name='Эл. почта')
    message = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return "Message from %s to %s" % (self.user, self.email)

