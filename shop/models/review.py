import os
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from core.models import HistoryModel


def review_image_upload_to(instance, filename):
	ymd_path = timezone.now().strftime('%Y%m%d')
	filename_base, filename_ext = os.path.splitext(filename) # 확장자 추출
	# return f'users/{_uuid}/profile/profile_{filename_base}_{ymd_path}{filename_ext}'
	return f'shop/review/%Y/%m/%d/image_{ymd_path}'

class Review(HistoryModel):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		related_name='%(class)s_user', 
		on_delete=models.CASCADE,
		verbose_name=_('작성자')
	)

	item = models.ForeignKey(
		to='shop.Item', 
		related_name='%(class)s_item', 
		on_delete=models.CASCADE,
		verbose_name=_('상품')
	)

	review = models.TextField(
		verbose_name=_('리뷰')
	)

	rating = models.IntegerField(
		validators=[MinValueValidator(1), MaxValueValidator(5)], 
		blank=True, 
		null=True,
		verbose_name=_('별점')
	)

	parent = models.ForeignKey(
		to='self', 
		related_name='replies',
		on_delete=models.CASCADE,
		null=True, 
		blank=True, 
		verbose_name=_('대댓글을 작성할 댓글')
	)

	class Meta:
		ordering = ['-id']
		db_table = 'review_tb'
		verbose_name = _('리뷰')
		verbose_name_plural = _('리뷰')

	def get_delete_url(self):
		return reverse('shop:review_delete', args=[self.product.pk, self.pk])


class ReviewImage(HistoryModel):
    review = models.ForeignKey(
		to='shop.Review', 
		related_name='%(class)s_review', 
		on_delete=models.CASCADE,
		verbose_name=_('리뷰')
	)

    image = models.ImageField(
		upload_to=review_image_upload_to, 
		blank=True,
		null=True,
		verbose_name=_('이미지')
	)