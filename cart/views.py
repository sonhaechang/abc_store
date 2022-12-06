import json
from django.db.models import F
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from rest_framework import status

from cart.models import Cart
from cart.services import SessionCart, cart_update_or_create

from shop.models import Item


# Create your views here.
def cart_list(request: HttpRequest) -> HttpResponse:
    ''' 징바구니 목록 '''

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).select_related('user')
    else:
        cart = SessionCart(request)

    return render(request, 'cart/container/cart_list.html', {
        'cart_list': cart,
    })

def add_cart(request: HttpRequest) -> JsonResponse:
    ''' 장바구니 저장 '''

    pk = request.POST.get('item_id')
    quantity = request.POST.get('quantity')
    item = get_object_or_404(Item, pk=pk)

    if request.user.is_authenticated:
        cart_qs = Cart.objects.filter(user=request.user, item=item)
        cart_update_or_create(request, item, cart_qs, quantity)
    else:
        cart = SessionCart(request)
        cart.add(item=item, quantity=str(quantity))

    return JsonResponse(data={'message': 'success'}, status=status.HTTP_200_OK)