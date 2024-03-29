import json
from typing import Any, Union

from django.http import (
    HttpRequest, HttpResponse, HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404

from cart.models import Cart

from shop.models import Item, ItemReal

RedirectOrResponse = Union[HttpResponseRedirect, HttpResponse, JsonResponse]


class CookieCart(object):
    ''' 쿠키 기반의 장바구니 클래스 (비로그인으로 장바구니 이용시 사용) '''

    def __init__(self, request: HttpRequest) -> None:
        ''' 초기화 '''

        self.request = request

    def __len__(self) -> int:
        ''' 쿠키 기반 장바구니에 저장 되어진 상품 전체 수량 반환 '''

        return sum(int(item) for item in self.get_cookies().values())

    def __iter__(self) -> dict[Any]:
        ''' Yield 활용한 쿠키 기반 장바구니에 저장 되어진 상품들을 generator해서 반환 '''

        for k, v in self.get_cookies().items():
            item = ItemReal.objects.get_or_none(pk=k)
            amount = item.get_amount()

            yield {
                'pk': k,
                'quantity': v,
                'total_amount': int(amount) * int(v),
                'item': {
                    'pk': item.pk,
                    'name': item.name,
                    'get_amount': amount,
                    'extra_amount': item.extra_amount,
                    'get_first_image': item.item.itemimage_item.first(),
                    'get_item_name': item.get_item_name(),
                    'is_public': item.is_public,
                }
            }

    def get_item_total(self) -> int:
        ''' 쿠키 기반 장바구니에 저장된 모든 상품의 총 금액 반환 '''

        item_amounts = list()

        for k, v in self.get_cookies().items():
            item = ItemReal.objects.get_or_none(pk=k)
            amount = item.get_amount()
            item_amounts.append(int(amount) * int(v))

        return sum(item_amounts)

    def get_cookies(self) -> dict[Any] | None:
        ''' 쿠키에 저장되어져 있는 장바구니 내역 가져와서 dict로 변환해서 반환 '''

        cart_list = self.request.COOKIES.get('cart_list', None)

        if cart_list is not None:
            json_cart_list = cart_list.replace("'","\"")
            cart_list = json.loads(json_cart_list)
            return cart_list
        return dict()

    def set_cookie(self, response: RedirectOrResponse, cart: dict) -> None:
        ''' 변동 사항 쿠키로 저장 '''

        response.set_cookie('cart_list', str(cart), max_age=86400*30)

    def delete_cookie(self, response: RedirectOrResponse) -> None:
        ''' 쿠키 삭제 '''

        response.delete_cookie('cart_list')

    def add(self, response: RedirectOrResponse, item_real_dict: dict[Any]) -> None:
        ''' 특정 상품을 쿠키 장바구니에 저장 '''

        cart_list = self.get_cookies()

        if cart_list:
            for pk, quantity in item_real_dict.items():
                quantity = int(cart_list[pk]) + int(quantity) if pk in cart_list else int(quantity)
                cart_list[pk] = 1 if quantity <= 0 else quantity
        else:
            for pk, quantity in item_real_dict.items():
                cart_list[pk] = quantity

        self.set_cookie(response, cart_list)

    def delete(self, response: RedirectOrResponse, pk: str) -> None:
        ''' 특정 상품을 쿠키 장바구니에서 제거 '''

        cart_list = self.get_cookies()

        if pk in cart_list:
            del cart_list[pk]

        self.set_cookie(response, cart_list)

def cart_update_or_create(request: HttpRequest, item_real_dict: dict[Any]) -> None:
    ''' 장바구니에 상품이 있으면 생성 없으면 추가 '''

    for pk, quantity in item_real_dict.items():
        item = get_object_or_404(ItemReal, pk=pk)
        cart = Cart.objects.get_or_none(user=request.user, item=item)
        
        if cart is None:
            Cart.objects.create(
                user=request.user,
                item=item,
                quantity=int(quantity))
        else:
            quantity = cart.quantity + int(quantity)
            cart.quantity = 1 if int(quantity) < 1 else quantity
            cart.save()

def anonymous_user_cart_to_db_cart(request: HttpRequest, cart_list: dict[Any]) -> None:
    ''' 세션 기반 장바구니의 내역을 장바구니 db에 저장'''
    
    if cart_list:
        cart_update_or_create(request, cart_list)


# class SessionCart(object):
#     ''' 세션 기반의 장바구니 클래스 (비로그인으로 장바구니 이용시 사용) '''

#     def __init__(self, request: HttpRequest) -> None:
#         ''' 초기화 '''

#         self.session = request.session

#         cart = self.session.get(settings.CART_ID)
#         self.cart = self.session[settings.CART_ID] = dict() if not cart else cart

#     def __len__(self) -> int:
#         ''' 세션 기반 장바구니에 저장 되어진 상품 전체 수량 반환 '''

#         return sum(item['quantity'] for item in self.cart.values())

#     def __iter__(self) -> dict[Any]:
#         ''' Yield 활용한 세션 기반 장바구니에 저장 되어진 상품들을 generator해서 반환 '''

#         for item in self.cart.values():
#             item['total_amount'] = item['item']['amount'] * item['quantity']
#             yield item

#     def save(self) -> None:
#         ''' 세션에 변동 사항(수정, 삭제)을 저장 '''

#         self.session[settings.CART_ID] = self.cart
#         self.session.modified = True

#     def add(self, item, quantity: int=1) -> None:
#         ''' 특정 상품을 세션 기반 장바구니에 저장 '''

#         item_id = str(item.id)

#         if item_id not in self.cart:
#             self.cart[item_id] = {'quantity': quantity} 
#             self.cart[item_id]['item'] = {
#                 'pk': item.pk,
#                 'name': item.name,
#                 'amount': item.sale_amount if item.sale_amount else item.amount,
#                 'get_first_image': item.itemimage_item.first(),
#                 'is_public': item.is_public,
#             }

#         self.cart[item_id]['quantity'] += int(quantity)

#         if self.cart[item_id]['quantity'] <= 0:
#             self.cart[item_id]['quantity'] = 1

#         self.save()

#     def remove(self, item: Model) -> None:
#         ''' 특정 상품을 세션 기반 장바구니에서 삭제 '''

#         item_id = str(item.id)

#         if item_id in self.cart:
#             del(self.cart[item_id])
#             self.save()

#     def clear(self) -> None:
#         ''' 세션 기반 장바구니에 저장된 모든 상품 삭제 '''

#         self.session[settings.CART_ID] = dict()
#         self.session.modified = True

#     def get_item_total(self) -> int:
#         ''' 세션 기반 장바구니에 저장된 모든 상품의 총 금액 반환 '''

#         return sum(int(item['item']['amount']) * int(item['quantity']) for item in self.cart.values())