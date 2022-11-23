from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from order.models import Order, OrderStatusLog


@receiver(pre_save, sender=Order)
def order_pre_save(sender, **kwargs):
	''' 등기번호 입력시 order의 status를 배송중으로 변경 및 order_item들의 status도 배송중으로 변경 '''

	order = kwargs['instance']

	if order.id and order.delivery_number and order.status == 'shipping_ready':
		order.status = 'shipping'

		for item in order.orderitem_order.all():
			if order.delivery_number and order.status == 'shipping' and item.status == 'paid':
				item.status = order.status
				item.save()

@receiver(post_save, sender=Order)
def order_post_save(sender, created, **kwargs):
	''' order의 status log 저장 '''

	order = kwargs['instance']
	OrderStatusLog.objects.create(order=order, status=str(order.status))


