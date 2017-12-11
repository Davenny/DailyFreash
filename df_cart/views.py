# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from .models import *
from df_user import user_decoratoe
from django.http import JsonResponse
# Create your views here.
@user_decoratoe.login
def my_cart(request):
    userId = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=userId)
    context = {
    'pagename':1,
        'carts':carts,
        'title':'My Cart',
    }
    return render(request,'df_cart/cart.html',context)

@user_decoratoe.login
def add(request,gid,count):
    userId = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=userId,goods_id=gid)

    if len(carts)>0:
        cart = carts[0]
        cart.count = cart.count+ int(count)
    else:
        cart = CartInfo()
        cart.user_id = userId
        cart.goods_id = gid
        cart.count = int(count)
    cart.save()
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        return JsonResponse({'count':count})
    else:
        return  redirect('/cart/')

@user_decoratoe.login
def edit(request,cart_id,count):
    try:
        cart = CartInfo.objects.get(pk = int(cart_id))
        count1 = cart.count = int(count)
        cart.save()
        data = {'ok':0}
    except Exception as e:
        data = {'ok':count1}
    return JsonResponse(data)

@user_decoratoe.login
def delete(request,cart_id):
    try:
        cart = CartInfo.objects.get(pk = int(cart_id))
        cart.delete()
        data = {'ok':1}
    except Exception as e:
        data = {'ok':0}
    return JsonResponse(data)