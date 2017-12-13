# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect
from django.shortcuts import render
from django.db import transaction
from df_user import user_decoratoe
from .models import *
import datetime
from df_cart.models import *
from decimal import Decimal

def myOrder(request):
    cart_ids = request.GET.getlist('cart_id')
    request.session['cart_ids'] = cart_ids
    carts=[]
    for cart_id in cart_ids:
        carts.append(CartInfo.objects.get(id=cart_id))
    context = {
        'pagename':1,
        'title':'Submit the order',
        'carts':carts,
    }
    return render(request,'df_order/place_order.html',context)

@transaction.atomic()
@user_decoratoe.login
def order_handle(request):
    tran_id = transaction.savepoint()
    cart_ids = request.session['cart_ids']
    try:
        order = OrderInfo()
        now = datetime.datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user = UserInfo.objects.get(pk = uid)
        order.odate = now
        print(request.POST.get('total'))
        order.ototal = Decimal(request.POST.get('total'))
        order.save()

        print(cart_ids)
        for id1 in cart_ids:
            print('--------'+id1)
            detail = OrderDetailInfo()
            detail.order = order
            cart = CartInfo.objects.get(id = id1)
            goods = cart.goods
            if goods.gkucun>=cart.count:
                goods.gkucun = cart.goods.gkucun - cart.count
                goods.save()
                detail.goods = goods
                detail.count = cart.count
                detail.price = cart.count * cart.goods.gprice
                detail.save()
                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print('===========================%s'%e)
        transaction.savepoint_rollback(tran_id)
    return redirect('/user/order/')