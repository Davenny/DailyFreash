# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from df_goods.models import *
from df_user.models import *

# Create your models here.
class CartInfo(models.Model):
    user = models.ForeignKey(UserInfo)
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField()