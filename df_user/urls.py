from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^register/$',views.register),
    url(r'^login/$',views.login),
    url(r'^register_exist/$',views.register_exist),
    url(r'^register_handle/$',views.register_handle),
    url(r'^info/$',views.info),
    url(r'login_handle/',views.login_handle),
    url(r'^user_center_info.html/$',views.info),
    url(r'^user_center_site.html/$',views.site),
    url(r'^user_center_order.html/$',views.userOrder),
    url(r'^logout/$',views.logout),
    url(r'order/',views.userOrder),
]
