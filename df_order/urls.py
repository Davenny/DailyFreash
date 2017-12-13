from django.conf.urls import url
import views
urlpatterns =[
    url(r'^$',views.myOrder),
    url(r'^handle/',views.order_handle),
]