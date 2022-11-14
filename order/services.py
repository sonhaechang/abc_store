from uuid import uuid4
from datetime import datetime, timedelta

from order.models import Order

class OrderInfo:
	def __init__(self, request, order_items):
		self.request = request
		self.order_items = order_items
		self.amount = sum(order_item.amount for order_item in order_items)

	def get_instance(self):
		user = self.request.user
		item = self.order_items[0]
		name = f'{item.item.name} 외 {len(self.order_items) - 1}건' \
			if len(self.order_items) > 1 else item.item.name

		instance = Order(
			name=name, 
			amount=self.amount,
			buyer_name= f'{user.last_name}{user.first_name}',
			merchant_uid=uuid4,
			buyer_postcode=user.postal_code,
			buyer_addr=user.address,
			detail_addr=user.detail_address,
			buyer_email=user.email,
			buyer_tel=user.phone,
		)

		return instance