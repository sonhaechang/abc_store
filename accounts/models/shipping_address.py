from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.validators import validate_phone_length

from core.models import HistoryModel


# Create your models here.
class ShippingAddress(HistoryModel):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE,
		verbose_name='사용자'
	)

	first_name = models.CharField(
		max_length=50, 
		verbose_name='성'
	)

	last_name = models.CharField(
		max_length=50, 
		verbose_name='이름'
	)

	postal_code = models.CharField(
		max_length=20, 
		verbose_name='우편번호'
	)

	address = models.CharField(
		max_length=100, 
		verbose_name='주소'
	)

	detail_address = models.CharField(
		max_length=100, 
		verbose_name='상세주소'
	)

	email = models.EmailField(
		verbose_name='email'
	)

	phone = models.CharField(
		max_length=11, 
		validators=[validate_phone_length], 
		verbose_name='전화번호'
	)


	class Meta:
		db_table = 'shipping_address_tb'
		verbose_name = _('배송지 정보')
		verbose_name_plural = _('배송지 정보')
