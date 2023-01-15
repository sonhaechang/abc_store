import json
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
		to='shop.Category', 
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

	supply_amount = models.PositiveSmallIntegerField(
		verbose_name=_('공급가액'),
		default=0
	)

	amount = models.PositiveSmallIntegerField(
		verbose_name=_('금액')
	)

	tax = models.PositiveSmallIntegerField(
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

	sale_amount = models.PositiveSmallIntegerField(
		blank=True, 
		null=True, 
		verbose_name=_('할인가')
	)

	#TODO: 추후 삭제 필요
	stock = models.PositiveSmallIntegerField(
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

	options = models.TextField(
		verbose_name=_('상품 옵션')
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

	def get_options(self):
		return json.loads(self.options)

	def is_one_item_real(self):
		values = self.get_options().values()

		if len(list(values)) == 1 and len(list(values)[0]) == 1:
			return True
		else:
			return False

	def get_absolute_url(self):
		return reverse(
			'shop:item_detail', 
			args=[self.category.category.slug, self.category.slug, self.slug]
		)


class ItemReal(HistoryModel):
	item = models.ForeignKey(
		to='shop.Item', 
		on_delete=models.CASCADE,
		related_name='%(class)s_item',
		verbose_name=_('상품')
	)

	name = models.CharField(
		max_length=100,
		verbose_name=_('옵션명')	
	)

	quantity = models.PositiveSmallIntegerField(
		default=0,
		verbose_name=_('수량')
	)

	safe_quantity = models.PositiveSmallIntegerField(
		default=0,
		verbose_name=_('안전 수량')
	)

	extra_amount = models.PositiveSmallIntegerField(
		default=0,
		verbose_name=_('추가 금액')
	)

	is_public = models.BooleanField(
		default=False, 
		db_index=True,
		verbose_name=_('판매 가능 여부')
	)

	class Meta:
		ordering = ['id']
		db_table = 'item_real_tb'
		verbose_name = _('상품 실물')
		verbose_name_plural = _('상품 실물')

	def get_amount(self):
		if self.item.sale_amount:
			return int(self.item.sale_amount) + int(self.extra_amount)
		else:
			return int(self.item.amount) + int(self.extra_amount)

	def is_extra_amount(self):
		if self.extra_amount > 0:
			return True
		else:
			return False


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