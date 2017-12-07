# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.paginator import Paginator

from django.shortcuts import render
from .models import *

# Create your views here.
def Index(request):
    typelist = TypeInfo.objects.all()
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    context = {'title':'首页','guest_cart':1,
               'type0':type0,'type01':type01}
    return render(request,'df_good/index.html',context)

def list(request,tid,pindex,sort):
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort=='1':
        good_list = GoodsInfo.objects.filter(gtype=int(tid)).order_by('-id')
    elif sort == '2':
        good_list = GoodsInfo.objects.filter(gtype=int(tid)).order_by('gprice')
    elif sort == '3':
        good_list = GoodsInfo.objects.filter(gtype=int(tid)).order_by('gclick')
    paginator = Paginator(good_list,3)
    page = paginator.page(int(pindex))
    context = {'title':typeinfo.title,'guest_cart':1,
               'page':page,
               'paginator':paginator,
               'typeinfo':typeinfo,
               'sort':sort,
               'news':news}
    return render(request,'df_good/list.html',context)

def detail(request,id):
    goods = GoodsInfo.objects.get(pk=int(id))
    goods.gclick = goods.gclick+1
    goods.save()
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {'title':goods.gtype.title,
               'id':id,
               'guest_cart':1,
               'g':goods,
               'news':news,
               'id':id}
    return render(request,'df_good/detail.html',context)

