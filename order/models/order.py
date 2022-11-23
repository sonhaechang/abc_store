import json
import pytz
from datetime import datetime
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import models
from django.http import Http404
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from iamport import Iamport

from accounts.validators import validate_phone_length

from core.models import HistoryModel

from order.enums import OrderStautsEnum, PayMethodEnum


def change_meta_to_json(meta):
	replace_meta = meta.replace("None", "null").replace(
		"False", "false").replace("True", "true").replace("'","\"")

	return json.loads(replace_meta)


def named_property(name):
    def wrap(fn):
        fn.short_description = name
        return property(fn)
    return wrap


def timestamp_to_datetime(timestamp):
    if timestamp:
        tz = pytz.timezone(settings.TIME_ZONE)
        return datetime.utcfromtimestamp(timestamp).replace(tzinfo=tz)
    return None


class Order(HistoryModel):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE,
		related_name='%(class)s_user',
		verbose_name=_('구매자')
	)

	merchant_uid = models.UUIDField(
		verbose_name=_('주문번호')
	)

	imp_uid = models.CharField(
		max_length=100, 
		blank=True, 
		verbose_name=_('아임포트 거래고유번호')
	)

	name = models.CharField(
		max_length=100, 
		verbose_name=_('상품명')
	)

	amount = models.PositiveIntegerField(
		verbose_name=_('결제금액')
	)

	delivery_amount = models.PositiveIntegerField(
		blank=True, 
		null=True, 
		verbose_name=_('배송비')
	)

	buyer_name = models.CharField(
		max_length=50, 
		verbose_name=_('이름')
	)

	buyer_postcode = models.CharField(
		max_length=20, 
		verbose_name=_('우편번호')
	)

	buyer_addr = models.CharField(
		max_length=100, 
		verbose_name=_('주소')
	)

	detail_addr = models.CharField(
		max_length=100, 
		verbose_name=_('상세주소')
	)

	buyer_email = models.EmailField(
		verbose_name=_('이메일')
	)

	buyer_tel = models.CharField(
		max_length=11, 
		# validators=[validate_phone_length], 
		verbose_name=_('전화번호')
	)

	exchange_return = models.BooleanField(
		default=False, 
		db_index=True, 
		verbose_name=_('교환/반품')
	)

	delivery_number = models.CharField(
		max_length=15, 
		blank=True, 
		verbose_name=_('등기번호')
	)

	status = models.CharField(
		max_length=17,
		choices=OrderStautsEnum.choices,
		default=OrderStautsEnum.ready,
		db_index=True,
		verbose_name=_('처리상태')
	)

	pay_method = models.CharField(
		max_length=5, 
		choices=PayMethodEnum.choices,
		default=PayMethodEnum.card,
		verbose_name=_('결제 수단')
	)

	vbank_num = models.CharField(
		max_length=50, 
		blank=True, 
		null=True,
		verbose_name=_('가상계좌')
	)

	meta = models.TextField(
		blank=True, 
		null=True,
		verbose_name=_('메타 데이터')
	)

	meta_json = named_property('메타 데이터')(lambda self: change_meta_to_json(self.meta) if self.meta else '')

	is_ready = property(lambda self: self.status == 'ready')
	is_paid = property(lambda self: self.status == 'paid')
	is_paid_ok = property(lambda self: self.status == 'paid' and self.amount == self.meta_json['amount'])

	is_cancelled = property(lambda self: self.status == 'cancelled')
	is_failed = property(lambda self: self.status == 'failed')

	is_re_receipt = property(lambda self: self.status == 're_receipt')

	is_shippable = property(lambda self: self.status == 'shippable')
	is_shipping = property(lambda self: self.status == 'shipping')
	is_delivered = property(lambda self: self.status == 'delivered')

	receipt_url = named_property(_('영수증'))(lambda self: self.meta_json['receipt_url'] if self.meta_json else '')
	cancel_reason = named_property(_('취소이유'))(lambda self: self.meta_json['cancel_reason'] if self.meta_json else '')
	fail_reason = named_property(_('실패이유'))(lambda self: self.meta_json['fail_reason'] if self.meta_json else '')
	card_name = named_property(_('카드정보'))(lambda self: self.meta_json['card_name'] if self.meta_json else '')

	paid_at = named_property(_('결제일시'))(lambda self: timestamp_to_datetime(self.meta_json['paid_at']) if self.meta_json else '')
	failed_at = named_property(_('실패일시'))(lambda self: timestamp_to_datetime(self.meta_json['failed_at']) if self.meta_json else '')
	cancelled_at = named_property(_('취소일시'))(lambda self: timestamp_to_datetime(self.meta_json['cancelled_at']) if self.meta_json else '')

	class Meta:
		db_table = 'order_tb'
		verbose_name = _('주문정보')
		verbose_name_plural = _('주문정보')
		ordering = ('-id',)


	def __str__(self):
		return self.imp_uid

	@property
	def api(self):
		'Iamport Client 인스턴스'
		return Iamport(settings.IAMPORT_API_KEY, settings.IAMPORT_API_SECRET)

	@named_property(_('결제금액'))
	def amount_html(self):
		return mark_safe('<div>{0}</div>'.format(intcomma(self.amount)))

	@named_property(_('처리결과'))
	def status_html(self):
		cls, text_color = '', ''
		help_text = ''
		if self.is_ready:
			cls, text_color = 'fa fa-shopping-cart', '#ccc'
		elif self.is_paid_ok:
			cls, text_color = 'fa fa-check-circle', 'green'
		elif self.is_cancelled:
			cls, text_color = 'fa fa-times', 'gray'
			help_text = self.cancel_reason
		elif self.is_failed:
			cls, text_color = 'fa fa-ban', 'red'
			help_text = self.fail_reason
		elif self.is_re_receipt:
			cls, text_color = 'fas fa-sync-alt', 'gray'

		elif self.is_shippable:
			cls, text_color = 'fas fa-dolly', 'gray'
		elif self.is_shipping:
			cls, text_color = 'fas fa-shipping-fast', 'gray'
		elif self.is_delivered:
			cls, text_color = 'fa fa-check-circle', '#3D77BD'
		html = '''
			<span style="color: {text_color};" title="this is title">
				<i class="{class_names}"></i>
				{label}
			</span>'''.format(class_names=cls, text_color=text_color, label=self.get_status_display())
		if help_text:
			html += f'<br/> <small>{help_text}</small>'
		return mark_safe(html)

	@named_property(_('영수증 링크'))
	def receipt_link(self):
		if self.is_paid and self.receipt_url:
			blank = "'_blank'"
			size = "'width=300, height=400'"
			return mark_safe(
				f'<a href="{self.receipt_url}" onclick="window.open({self.receipt_url}, {blank}, {size})">영수증</a>')

	def is_card(self):
		if self.pay_method == 'card':
			return True
		else:
			return False

	def is_trans(self):
		if self.pay_method == 'trans':
			return True
		else:
			return False

	def is_vbank(self):
		if self.pay_method == 'vbank':
			return True
		else:
			return False

	def is_phone(self):
		if self.pay_method == 'phone':
			return True
		else:
			return False

	def update(self, commit=True, meta=None):
		''' 결재내역 갱신 '''

		if self.imp_uid:
			try:
				self.meta = meta or self.api.find(imp_uid=self.imp_uid)
				val = meta or self.api.find(imp_uid=self.imp_uid)
			except Iamport.HttpError:
				raise Http404(f'Not found {self.imp_uid}')

			# merchant_uid는 반드시 매칭되어야 합니다.
			assert str(self.merchant_uid) == val['merchant_uid']
			if self.status != 'exchange_return' and self.status != 'shipping_ready' \
				and self.status != 'shipping' and self.status != 'shipping_complete':
				self.status = val['status']
			self.pay_method = val['pay_method']
		if commit:
			self.save()

	def cancel(self, reason=None, amount=None, commit=True):
		''' 결제내역 취소 '''
		
		try:
			meta = self.api.cancel(reason, imp_uid=self.imp_uid, amount=amount)
			val = meta or self.api.find(imp_uid=self.imp_uid)
			assert str(self.merchant_uid) == val['merchant_uid']
			self.update(commit=commit, meta=meta)

		# 취소시 오류 예외처리(이미 취소된 결제는 에러가 발생함)
		except Iamport.ResponseError as e:
			self.update(commit=commit)
		if commit:
			self.save()
