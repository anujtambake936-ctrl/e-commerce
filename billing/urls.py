from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^checkout/$', views.checkout_home, name='checkout'),
    url(r'^payment/$', views.payment_method_createview, name='payment'),
    url(r'^payment/success/(?P<order_id>[\w-]+)/$', views.payment_success, name='payment_success'),
    url(r'^orders/$', views.order_history, name='order_history'),
]

