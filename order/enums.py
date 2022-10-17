from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

class OrderStautsEnum(TextChoices):
	""" 주문 상태 구분 클래스 """

	ready = 'ready', _('미결제')
	paid = 'paid', _('결제완료')
	cancelled = 'cancelled', _('결제취소')
	failed = 'failed', _('결제실패')
	exchange_return ='exchange_return', _('교환/반품'),
	shipping_ready = 'shipping_ready', _('배송준비'),
	shipping = 'shipping', _('배송중'),
	shipping_complete = 'shipping_complete', _('배송완료'),


class OrderItemStatusEnum(TextChoices):
	""" 주문 상품 상태 구분 클래스 """

	ready = 'ready', _('미결제')
	paid = 'paid', _('결제완료')
	cancelled = 'cancelled', _('결제취소')
	failed = 'failed', _('결제실패')
	exchange_return ='exchange_return', _('교환/반품'),
	shipping_ready = 'shipping_ready', _('배송준비'),
	shipping = 'shipping', _('배송중'),
	shipping_complete = 'shipping_complete', _('배송완료'),

	exchange_ready = 'exchange_ready', _('교환접수요청'),
	exchange_receipt = 'exchange_receipt', _('교환접수'),
	exchanging = 'exchanging', _('교환처리중'),
	exchange_complete = 'exchange_complete', _('교환완료'),
	exchange_fail = 'exchange_fail', _('교환실패'),
	exchange_cancel = 'exchange_cancel', _('교환취소'),
	return_ready = 'return_ready', _('반품접수요청'),
	return_receipt = 'return_receipt', _('반품접수'),
	returning = 'returning', _('반품처리중'),
	return_complete = 'return_complete', _('반품완료'),
	return_fail = 'return_fail', _('반품실패'),
	return_cancel = 'return_cancel', _('반품취소'),


class PayMethodEnum(TextChoices):
	""" 결제 방식 구분 클래스 """

	card = 'card', _('신용카드')
	trans = 'trans', _('실시간계좌이체')
	vbank = 'vbank', _('가상계좌')
	phone = 'phone', _('휴대폰소액결제')