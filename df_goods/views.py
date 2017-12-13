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
               'news':news,
               'need_new':1,}
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
    re = render(request,'df_good/detail.html',context)

    goods_ids = request.COOKIES.get('goods_ids','')
    goods_id = '%d'%goods.id
    if goods_ids!='':
        goods_ids1 = goods_ids.split(',')
        if goods_ids1.count(goods_id)>=1:
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0,goods_id)
        if len(goods_ids1)>=6:
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)
        print(goods_ids1)
    else:
        goods_ids = goods_id
    print(goods_ids)
    re.set_cookie('goods_ids',goods_ids)
    return re



