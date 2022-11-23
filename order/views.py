from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from order.forms import OrderForm
from order.models import Order, OrderItem
from order.services import OrderInfo, OrderItemHandler

from shop.models import Item


# Create your views here.
@login_required
def order_pay(request):
	item_qs = Item.objects.filter(id__in=request.GET.keys())
	quantity_dict = { int(k): int(v) for k, v in request.GET.dict().items() }

	order_items = list()
	for item in item_qs:
		quantity = quantity_dict[item.pk]
		order_item = OrderItem(quantity=quantity, item=item)
		order_items.append(order_item)

	order_info = OrderInfo(request, order_items)
	instance = order_info.get_instance()
	
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

			return redirect('order:order_complete', str(order.merchant_uid))
	else:
		form = OrderForm(instance=instance)

	data = {
		'form': form,
		'order_items': order_items,
		'iamport_shop_id': settings.IAMPORT_SHOP_ID
	}

	return render(request, 'order/container/order_pay.html', data)

@login_required
def order_complete(request, merchant_uid):
	order = Order.objects.get_or_none(merchant_uid=merchant_uid)

	return render(request, 'order/container/order_complete.html', {
		'order': order,
	})