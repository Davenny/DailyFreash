from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$',views.Index),
    url(r'^list(\d+)_(\d+)_(\d+)/$',views.list),
    url(r'^(\d+)/$',views.detail),
]