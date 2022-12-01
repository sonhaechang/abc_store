from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from core.models import HistoryModel

from shop.models import Item


# Create your models here.
class Cart(HistoryModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_user', 
        on_delete=models.CASCADE,
        verbose_name=_('구매자')
    )

    item = models.ForeignKey(
        to='shop.Item', 
        related_name='%(class)s_item', 
        on_delete=models.CASCADE,
        verbose_name=_('상품')
    )

    quantity = models.PositiveSmallIntegerField(
        verbose_name=_('수량')
    )

    class Meta:
        ordering = ['-id']
        db_table = 'cart_tb'
        verbose_name = _('장바구니')
        verbose_name_plural = _('장바구니')
        

    def __str__(self):
        return self.user.username

    def total_amount(self):
        if self.item.sale_amount:
            return self.quantity * self.item.sale_amount
        else:
            return self.quantity * self.item.amount