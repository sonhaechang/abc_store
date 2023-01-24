from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import HistoryModel

from order.enums import OrderItemStatusEnum


class OrderItem(HistoryModel):
	order = models.ForeignKey(
		to='order.Order', 
		on_delete=models.CASCADE,
		related_name='%(class)s_order',
		verbose_name=_('주문정보')
	)

	item = models.ForeignKey(
		to='shop.ItemReal', 
		on_delete=models.CASCADE, 
		related_name='%(class)s_item',
		verbose_name=_('상품실물')
	)

	quantity = models.PositiveIntegerField(
		verbose_name=_('수량')
	)

	delivery_number = models.CharField(
		max_length=15, 
		blank=True, 
		verbose_name=_('등기번호')
	)

	status = models.CharField(
		max_length=17,
		choices=OrderItemStatusEnum.choices,
		default=OrderItemStatusEnum.ready,
		db_index=True,
		verbose_name=_('처리상태'),
	)

	class Meta:
		ordering = ['-id']
		db_table = 'order_item_tb'
		verbose_name = _('주문상품')
		verbose_name_plural = _('주문상품')

	def __str__(self):
		return self.item.name

	@property
	def amount(self):
		return self.quantity * self.item.get_amount()