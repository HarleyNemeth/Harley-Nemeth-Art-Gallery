from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('store/', views.store, name='store'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:artwork_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:artwork_id>/', views.remove_from_cart, name='remove_from_cart'),
]