# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from hashlib import sha1
from django.http import JsonResponse,HttpResponseRedirect
# Create your views here.from hashlib import sha1
from django.shortcuts import render,redirect
from models import *
import user_decoratoe
from df_goods.models import *
from df_order.models import *

def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    if upwd!=upwd2:
        return redirect('/user/register/')

    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()
    user = UserInfo()
    user.uname = uname
    user.upwd =upwd3
    user.uemail =uemail
    user.save()
    return redirect('/user/login/')

def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'User Login','error_name':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu',0)

    users = UserInfo.objects.filter(uname=uname)
    if len(users)==1:
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upwd:
            url = request.COOKIES.get('url','/')
            red = HttpResponseRedirect(url)

            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title':'User Login','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request,'df_user/login.html',context)
    else:
        context = {'title':'User Login','error_name':1,'error_pwd':0,'uname':uname,'upwd':upwd}
        return render(request,'df_user/login.html',context)


def logout(request):
    request.session.flush()
    return redirect('/')



@user_decoratoe.login
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    goods_ids = request.COOKIES.get('goods_ids','')
    goods_ids1 = goods_ids.split(',')
    goods_list = []
    for good_id in goods_ids1:
        print(good_id)
        if good_id!='':
            goods_list.append(GoodsInfo.objects.get(id=int(good_id)))

    context= {
        'title':'User Zone',
        'user_email':user_email,
        'user_name':request.session['user_name'],
        'pagename':1,
        'goods_List':goods_list,
    }
    return render(request,'df_user/user_center_info.html',context)

@user_decoratoe.login
def site(request):
    user = UserInfo.objects.get(id = request.session['user_id'])
    if request.method=='POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title':'User Zone','user':user,'page_name':1}
    return render(request,'df_user/user_center_site.html',context)

@user_decoratoe.login
def userOrder(request):
    user_id = request.session['user_id']
    my_order = OrderInfo.objects.filter(user_id=user_id)
    my_order_detail = OrderDetailInfo.objects.filter(order__in=my_order)
    print('--------------------')
    print(my_order_detail)
    print(my_order)
    context = {
        'title':'User Zone',
        'my_order':my_order,
        'my_order_detail':my_order_detail,
    }
    return render(request,'df_user/user_center_order.html',context)