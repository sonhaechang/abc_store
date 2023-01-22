import json

from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render

from rest_framework import status

from cart.models import Cart
from cart.services import CookieCart, cart_update_or_create

from shop.models import ItemReal


# Create your views here.
def cart_list(request: HttpRequest) -> HttpResponse:
    ''' 징바구니 목록 '''

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).select_related('user')
        get_item_total = sum(item.quantity * item.item.get_amount() for item in cart)
    else:
        cart = CookieCart(request)
        get_item_total = cart.get_item_total()

    return render(request, 'cart/container/cart_list.html', {
        'cart_list': cart,
        'get_item_total': get_item_total
    })

def add_cart(request: HttpRequest) -> JsonResponse:
    ''' 장바구니 저장 '''

    item_real_dict = request.POST.get('item_reals')
    response = JsonResponse(data={'message': 'success'}, status=status.HTTP_200_OK)

    if request.user.is_authenticated:
        cart_update_or_create(request, json.loads(item_real_dict))
    else:
        cookie_cart = CookieCart(request)
        cookie_cart.add(response, json.loads(item_real_dict))

    return response

def delete_cart(request: HttpRequest, item_pk: str) -> JsonResponse:
    ''' 장바구니 삭제 '''

    item = ItemReal.objects.get_or_none(id=item_pk)
    data = {'message': '삭제했습니다.'}
    status_code = status.HTTP_200_OK
    response = JsonResponse(data=data, status=status_code)
    
    if item is None:
        data = {'error': '404 (Not Found)'}
        status_code = status.HTTP_404_NOT_FOUND
        return JsonResponse(data, status_code)

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, item=item)
        if cart:
            cart.delete()
        else:
            data = {'error': '404 (Not Found)'}
            status_code = status.HTTP_404_NOT_FOUND
            return JsonResponse(data=data, status=status_code)
    else:
        cart = CookieCart(request)
        cart.delete(response, str(item_pk))
    
    return response