from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404

from rest_framework import status

from cart.models import Cart
from cart.services import CookieCart, cart_update_or_create

from shop.models import Item


# Create your views here.
def cart_list(request: HttpRequest) -> HttpResponse:
    ''' 징바구니 목록 '''

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).select_related('user')
        get_item_total = sum(item.quantity * item.item.amount for item in cart)
    else:
        cart = CookieCart(request)
        get_item_total = cart.get_item_total()

    return render(request, 'cart/container/cart_list.html', {
        'cart_list': cart,
        'get_item_total': get_item_total
    })

def add_cart(request: HttpRequest) -> JsonResponse:
    ''' 장바구니 저장 '''

    pk = request.POST.get('item_id')
    quantity = request.POST.get('quantity')
    item = get_object_or_404(Item, pk=pk)

    response = JsonResponse(data={'message': 'success'}, status=status.HTTP_200_OK)

    if request.user.is_authenticated:
        cart_qs = Cart.objects.filter(user=request.user, item=item)
        cart_update_or_create(request, item, cart_qs, quantity)
    else:
        cookie_cart = CookieCart(request)
        cookie_cart.add(response, pk, quantity)

    return response

def delete_cart(request: HttpRequest, item_pk: str) -> JsonResponse:
    ''' 장바구니 삭제 '''

    item = get_object_or_404(Item, id=item_pk)
    response = JsonResponse(data={'message': '삭제했습니다.'}, status=status.HTTP_200_OK)

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, item=item)
        cart.delete()
    else:
        cart = CookieCart(request)
        cart.delete(response, str(item_pk))
    
    return response