from django.urls import path

from . import views

urlpatterns = [
    path('', views.homePage, name='home page'),
    path('add', views.addToCart, name="add to cart"),
    path('cart', views.showCart, name='cart'),
    path('cart/update', views.updateCart, name='update cart'),
    path('cart/checkout', views.checkOut, name='checkout'),
    path('cart/clear', views.clearCart, name='clear cart'),
]