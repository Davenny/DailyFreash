# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','uname']

# Register your models here.
admin.site.register(UserInfo,UserAdmin)