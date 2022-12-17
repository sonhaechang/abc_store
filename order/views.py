import json

from typing import Any, Dict, Union

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import (
	HttpResponse, HttpRequest, HttpResponseRedirect, 
	JsonResponse,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from rest_framework import status

from cart.models import Cart

from core.mixins import PaginationsMixins

from order.enums import OrderStautsEnum
from order.forms import OrderForm
from order.models import Order
from order.services import OrderInfo, OrderItemHandler

RedirectOrResponse = Union[HttpResponseRedirect, HttpResponse]


# Create your views here.
class OrderListView(LoginRequiredMixin, PaginationsMixins, ListView):
	''' 사옹자별 주문(결제) 목록 확인 '''

	template_name = 'order/container/order_list.html'

	def get_queryset(self, **kwargs: Any) -> QuerySet:
		return Order.objects.filter(user=self.request.user).select_related('user')

	def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
		context = super().get_context_data(**kwargs)
		status = OrderStautsEnum
		queryset = self.get_queryset()

		context['ready'] = queryset.filter(status=status.ready).count()
		context['paid'] = queryset.filter(status=status.paid).count()
		context['shipping'] = queryset.filter(status=status.shipping).count()
		context['shipping_complete'] = queryset.filter(status=status.shipping_complete).count()
		context['exchange_return'] = queryset.filter(exchange_return='True').count()

		return context


@login_required
def order_detail(request: HttpRequest, merchant_uid:str) -> HttpResponse:
	''' 사용자별 주문 상세 '''

	order = get_object_or_404(Order, user=request.user, merchant_uid=merchant_uid)
	total_quantity =  order.orderitem_order.count()

	return render(request, 'order/container/order_detail.html', {
		'order': order,
		'total_quantity': total_quantity,
	})

@login_required
def order_item_save_in_session(request: HttpRequest) -> JsonResponse:
	''' 장바구니에 저장된 주문할 상품 세션에 저장 '''

	if request.session.get('order_items'):
		request.session['order_items'] = None

	if request.method == 'POST':
		cart_qs = Cart.objects.filter(id__in=json.loads(request.POST.get('cart_ids')))
		item_qs = dict()
		for cart in cart_qs:
			item_qs[cart.item.id] = cart.quantity
		request.session['order_items'] = item_qs

		return JsonResponse(
			data={'redirect_url': reverse('order:order_pay')}, 
			status=status.HTTP_200_OK
		)
	else:
		return JsonResponse(
			data={'error': 'Method Not Allowed'}, 
			status=status.HTTP_405_METHOD_NOT_ALLOWED
		)

@login_required
def order_pay(request: HttpRequest) -> RedirectOrResponse:
	order_info = OrderInfo(request)
	order_items, instance = order_info.get_instance()

	m_redirect_url = f'{get_current_site(request).domain}{reverse("order:order_complete_mobile")}'

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=instance)
		if form.is_valid():
			order = form.save(commit=False)
			order.user = request.user
			order.merchant_uid = form.cleaned_data['merchant_uid']
			order.imp_uid = form.cleaned_data['imp_uid']
			order.save()

			order_item_handler = OrderItemHandler(order)
			order_item_handler.create_order_items(order_items)
			order_item_handler.stock_minus_counter()

			del request.session['order_items']

			return redirect('order:order_complete', str(order.merchant_uid))
	else:
		form = OrderForm(instance=instance)

	return render(request, 'order/container/order_pay.html', {
		'form': form,
		'order_items': order_items,
		'iamport_shop_id': settings.IAMPORT_SHOP_ID,
		'm_redirect_url': m_redirect_url
	})

@login_required
def order_complete(request: HttpRequest, merchant_uid: str) -> HttpResponse:
	order = get_object_or_404(Order, user=request.user, merchant_uid=merchant_uid)

	return render(request, 'order/container/order_complete.html', {
		'order': order,
	})

@login_required
def order_complete_mobile(request: HttpRequest) -> HttpResponseRedirect:
	''' 모바일로 결제시 iamport에서 처리 결과를 받아 db에 저장 '''

	imp_uid = request.GET.get('imp_uid')
	merchant_uid = request.GET.get('merchant_uid')
	imp_success = request.GET.get('imp_success')

	order_info = OrderInfo(request)
	order_items, order = order_info.get_instance()

	if imp_success == 'true':
		order.user=request.user
		order.merchant_uid=merchant_uid
		order.imp_uid=imp_uid
		order.save()
		order.update()

		order_item_handler = OrderItemHandler(order)
		order_item_handler.create_order_items(order_items)
		order_item_handler.stock_minus_counter()

		del request.session['order_items']
	return redirect('order:order_complete', str(order.merchant_uid))

@login_required
def order_cancel(request: HttpRequest, merchant_uid: str) -> HttpResponseRedirect:
	''' 주문 취소 '''

	# TODO: redirect가 아닌 JsonResponse로 수정하는 방법도 고려해볼법함  
	order = get_object_or_404(Order, user=request.user, merchant_uid=merchant_uid)

	if order.user == request.user:
		order.cancel()
		order_item_handler = OrderItemHandler(order)
		order_item_handler.set_cancel_status()
		order_item_handler.stock_plus_counter()
		return redirect('order:order_detail', order.merchant_uid)
	else:
		raise PermissionDenied