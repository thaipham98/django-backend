from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from shop.models import Product
from shop.serializer import ProductSerializer

product1 = Product(id=1, name='Mac Air', detail='M1 chip')
product2 = Product(id=2, name='Mac Pro 13', detail='M2 chip')
product3 = Product(id=3, name='Mac Pro 14', detail='M2 Pro chip')

db = {1: product1, 2: product2, 3: product3}
cart = {}


def index(request):
    return HttpResponse("Hello, world!")


# Create your views here.
@api_view(['GET'])
def homePage(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addToCart(request):
    id = request.data.get("id")

    if id not in cart:
        cart[id] = 0
    cart[id] += 1
    serializer = ProductSerializer(db[id])
    return Response(serializer.data)


@api_view(['GET'])
def showCart(request):
    cartResponse = {}
    for id in cart.keys():
        product = db[id]
        cartResponse[id] = {"name": product.name, "detail": product.detail, "quantity": cart[id]}

    return Response(cartResponse)


@api_view(['POST'])
def updateCart(request):
    id = request.data.get("id")
    quantity = request.data.get("quantity")

    if id not in cart:
        return Response("Failure", status=status.HTTP_404_NOT_FOUND)

    cart[id] += quantity

    if cart[id] <= 0:
        cart.pop(id)

    cartResponse = {}
    for id in cart.keys():
        product = db[id]
        cartResponse[id] = {"name": product.name, "detail": product.detail, "quantity": cart[id]}

    return Response(cartResponse)


@api_view(['GET'])
def checkOut(request):
    if len(cart) == 0:
        return Response("There are no items in your cart")

    cart.clear()
    return Response("Purchased!")


@api_view(['GET'])
def clearCart(request):
    if len(cart) == 0:
        return Response("There are no items in your cart")

    cart.clear()
    return Response("Cart cleared")
