import os
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from core.models import HistoryModel


def item_image_upload_to(instance, filename):
	ymd_path = timezone.now().strftime('%Y%m%d')
	filename_base, filename_ext = os.path.splitext(filename) # 확장자 추출
	# return f'users/{_uuid}/profile/profile_{filename_base}_{ymd_path}{filename_ext}'
	return f'shop/itme/%Y/%m/%d/image_{ymd_path}'


class Item(HistoryModel):
	category = models.ForeignKey(
		to='shop.CategoryDetail', 
		on_delete=models.SET_NULL, 
		related_name='%(class)s_category',
		null=True,
		verbose_name=_('카테고리')
	)

	name = models.CharField(
		max_length=100, 
		db_index=True, 
		verbose_name=_('상품명')
	)

	slug = models.SlugField(
		max_length=100, 
		db_index=True, 
		unique=True, 
		allow_unicode=True,
		verbose_name=_('슬러그 필드')
	)

	description = models.TextField(
		blank=True, 
		verbose_name=_('설명')
	)

	supply_price = models.PositiveIntegerField(
		verbose_name=_('공급가액'),
		default=0
	)

	amount = models.PositiveIntegerField(
		verbose_name=_('금액')
	)

	tax = models.PositiveIntegerField(
		verbose_name=_('세금'),
		default=0
	)

	sale_percent = models.DecimalField(
		max_digits=4, 
		decimal_places=2,
		blank=True, 
		null=True, 
		verbose_name=_('할인율')
	)

	sale_amount = models.PositiveIntegerField(
		blank=True, 
		null=True, 
		verbose_name=_('할인가')
	)

	stock = models.PositiveIntegerField(
		verbose_name=_('수량')
	)

	is_halal = models.BooleanField(
		default=False, 
		db_index=True, 
		verbose_name=_('할랄')
	)

	is_public = models.BooleanField(
		default=False, 
		db_index=True,
		verbose_name=_('판매 가능 여부')
	)

	best_item = models.BooleanField(
		default=False, 
		db_index=True,
		verbose_name=_('베스트 아이템')
	)

	class Meta:
		ordering = ['-id']
		db_table = 'item_tb'
		verbose_name = _('상품')
		verbose_name_plural = _('상품')

	def __str__(self):
		return self.name

	def get_first_image(self):
		return self.itemimage_item.first()

	def get_absolute_url(self):
		return reverse(
			'shop:item_detail', 
			args=[self.category.category.slug, self.category.slug, self.slug]
		)


class ItemImage(HistoryModel):
	item = models.ForeignKey(
		to='shop.Item', 
		on_delete=models.CASCADE,
		related_name='%(class)s_item',
		verbose_name=_('상품')
	)

	image = models.ImageField(
		upload_to='item_image_upload_to',
		blank=True,
		null=True,
		verbose_name=_('상품 이미지')
	)

	class Meta:
		ordering = ['-id']
		db_table = 'item_image_tb'
		verbose_name = _('상품 이미지')
		verbose_name_plural = _('상품 이미지')

	def __str__(self):
		return self.item.name