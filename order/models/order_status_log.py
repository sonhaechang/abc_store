from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import HistoryModel

from order.enums import OrderStautsEnum


class OrderStatusLog(HistoryModel):
	order = models.ForeignKey(
		to='order.Order', 
		on_delete=models.CASCADE,
		related_name='%(class)s_order',
		verbose_name=_('주문정보')
	)

	status = models.CharField(
		max_length=17,
		choices=OrderStautsEnum.choices,
		default=OrderStautsEnum.ready,
		db_index=True,
		verbose_name=_('처리상태')
	)

	class Meta:
		db_table = 'order_status_log_tb'
		verbose_name = _('주문 처리상태 로그')
		verbose_name_plural = _('주문 처리상태 로그')
		ordering = ('-created_at',)

	def __str__(self):
		return self.order.name