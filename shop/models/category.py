import os
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from core.models import HistoryModel


# Create your models here.
def category_thumbnail_upload_to(instance, filename):
	ymd_path = timezone.now().strftime('%Y%m%d')
	filename_base, filename_ext = os.path.splitext(filename) # 확장자 추출
	# return f'users/{_uuid}/profile/profile_{filename_base}_{ymd_path}{filename_ext}'
	return f'shop/category/thumbnail/thumbnail_{ymd_path}'

def category_detail_thumbnail_upload_to(instance, filename):
	ymd_path = timezone.now().strftime('%Y%m%d')
	filename_base, filename_ext = os.path.splitext(filename) # 확장자 추출
	# return f'users/{_uuid}/profile/profile_{filename_base}_{ymd_path}{filename_ext}'
	return f'shop/category/detail/thumbnail/thumbnail_{ymd_path}'


class Category(HistoryModel):
	name = models.CharField(
		max_length=100, 
		db_index=True,
		verbose_name=_('카테고리 이름')
	)

	slug = models.SlugField(
		max_length=100, 
		db_index=True, 
		unique=True, 
		allow_unicode=True,
		verbose_name=_('슬러그 필드')
	)

	thumbnail = models.ImageField(
		upload_to=category_thumbnail_upload_to, 
		blank=True,
		null=True,
		verbose_name=_('썸네일')
	)

	class Meta:
		db_table = 'category_tb'
		verbose_name = _('카테고리')
		verbose_name_plural = _('카테고리')

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:category_detail', args=[self.slug])


class CategoryDetail(HistoryModel):
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
		verbose_name=_('세부 카테고리 이름')
	)

	slug = models.SlugField(
		max_length=100, 
		db_index=True, 
		unique=True, 
		allow_unicode=True,
		verbose_name=_('슬러그 필드')
	)

	thumbnail = models.ImageField(
		upload_to=category_detail_thumbnail_upload_to, 
		blank=True,
		null=True,
		verbose_name=_('썸네일')
	)

	class Meta:
		db_table = 'category_detail_tb'
		verbose_name = _('세부 카테고리')
		verbose_name_plural = _('세부 카테고리')

	def __str__(self):
		return self.name