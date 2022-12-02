from decimal import Decimal
import json
from typing import Any

from django.conf import settings
from django.db.models import F, Model
from django.http import HttpRequest

from cart.models import Cart

from shop.models import Item


class SessionCart(object):
    ''' 세션 기반의 장바구니 클래스 (비로그인으로 장바구니 이용시 사용) '''

    def __init__(self, request: HttpRequest) -> None:
        ''' 초기화 '''

        self.session = request.session
        cart = self.session[settings.CART_ID]
        self.cart = self.session[settings.CART_ID] = dict() if not cart else cart

    def __len__(self) -> int:
        ''' 세션 기반 장바구니에 저장 되어진 상품 전체 수량 반환 '''

        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self) -> Model:
        ''' Yield 활용한 세션 기반 장바구니에 저장 되어진 상품들을 generator해서 반환 '''

        for item in Item.objects.filter(id__in=self.cart.keys()):
            self.cart[str(item.id)]['item'] = item

        for item in self.cart.values():
            item['amount'] = Decimal(item['amount'])
            item['total_amount'] = item['amount'] * item['quantity']

            yield item

    def save(self) -> None:
        ''' 세션에 변동 사항(수정, 삭제)을 저장 '''

        self.session[settings.CART_ID] = self.cart
        self.session.modified = True

    def add(self, item, quantity=1) -> None:
        ''' 특정 상품을 세션 기반 장바구니에 저장 '''

        item_id = str(item.id)

        if item_id not in self.cart:
            self.cart[item_id] = {'quantity':0, 'amount':str(item.sale_amount)} \
                if item.sale_amount else {'quantity':0, 'amount':str(item.amount)}

        self.cart[item_id]['quantity'] += int(quantity)

        if self.cart[item_id]['quantity'] <= 0:
            self.cart[item_id]['quantity'] = 1

        self.save()

    def remove(self, item) -> None:
        ''' 특정 상품을 세션 기반 장바구니에서 삭제 '''

        item_id = str(item.id)

        if item_id in self.cart:
            del(self.cart[item_id])
            self.save()

    def clear(self) -> None:
        ''' 세션 기반 장바구니에 저장된 모든 상품 삭제 '''

        self.session[settings.CART_ID] = dict()
        self.session.modified = True

    def get_item_total(self) -> int:
        ''' '''

        return sum(Decimal(item['amount'])*item['quantity'] for item in self.cart.values())


def get_cookies(request: HttpRequest) -> dict[Any] | None:
    ''' 쿠키에 저장되어져 있는 장바구니 내역 가져와서 dict로 변환해서 반환 '''

    cart_list = request.COOKIES.get('cart_list', None)

    if cart_list is not None:
        json_cart_list = cart_list.replace("'","\"")
        cart_list = json.loads(json_cart_list)

    return cart_list

def session_cart_to_models_cart(request: HttpRequest) -> None:
    ''' 세션 기반 장바구니의 내역을 장바구니 db에 저장'''

    cart_list = get_cookies(request)
    
    if cart_list:
        for item in Item.objects.filter(id__in=cart_list.keys()):
            cart_qs = Cart.objects.filter(user=request.user, item=item)
            quantity = int(cart_list[str(item.pk)]['quantity'])

            if not cart_qs.exists():
                Cart.objects.create(
                    user=request.user,
                    item=item,
                    quantity=quantity)
            else:
                cart_qs.update(quantity=F('quantity') + quantity)