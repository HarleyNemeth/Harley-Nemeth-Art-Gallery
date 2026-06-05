from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery/', views.gallery, name='gallery'),
    path('store/', views.store, name='store'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
]