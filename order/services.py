from uuid import uuid4

from django.db.models import F

from order.models import Order, OrderItem


class OrderInfo:
	''' 주문정보 생성하는 class '''

	def __init__(self, request, order_items):
		self.request = request
		self.order_items = order_items
		self.amount = sum(order_item.amount for order_item in order_items)

	def get_instance(self):
		''' create order instance '''

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


class OrderItemHandler:
	''' 주문상품을 handling하는 class '''

	def __init__(self, order):
		self.order = order
		self.order_items = order.orderitem_order.all()

	def create_order_items(self, order_items):
		''' 주문상품을 bulk_create로 생성 '''

		for order_item in order_items:
			order_item.order = self.order
			order_item.status = self.order.status

		OrderItem.objects.bulk_create(order_items)

	def set_paid_status(self):
		''' 주문상품의 status를 order의 status(paid)로 변경 '''

		if not self.order.status == 'exchange_return':
			self.order_items.update(status=self.order.status)

	def set_cancel_status(self):
		''' order_item의 status를 주문취소로 변경 '''

		self.order_items.update(status='cancelled')

	def stock_minus_counter(self):
		''' item 수량을 order_item 수만큼 차감 '''

		if self.order.status == 'paid':
			for order_item in self.order_items:
				item = order_item.item
				item.stock = int(item.stock) - int(order_item.quantity)

				if item.stock == 0:
					item.is_public = False
				item.save()

	def stock_plus_counter(self):
		''' item 수량을 order_item 수만큼 가감 '''

		for order_item in self.order_items:
			item = order_item.item
			item.stock = int(item.stock) + int(order_item.quantity)

			if item.stock > 0:
				item.is_public = True
			item.save()