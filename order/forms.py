from django import forms
from django.utils.translation import gettext_lazy as _

from order.models import Order
from order.enums import PayMethodEnum

class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['pay_method', 'buyer_name', 'buyer_tel', 'buyer_email', 'pay_method',
			'buyer_postcode', 'buyer_addr', 'detail_addr', 'imp_uid', 'merchant_uid', 'vbank_num'
		]

		widgets = {
			'imp_uid': forms.HiddenInput,
			'merchant_uid': forms.HiddenInput,
			'vbank_num': forms.HiddenInput,
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# class_update_fields = self.fields

		# for field_name in class_update_fields:
		# 	self.fields[field_name].widget.attrs.update({'class': 'form-control'})

		self.fields['pay_method'] = forms.ChoiceField(
			label='pay_method', choices=PayMethodEnum.choices, required=True, widget=forms.RadioSelect())

		self.fields['buyer_name'].label = _('이름')
		self.fields['buyer_name'].widget.attrs['placeholder'] = _('이름')

		self.fields['buyer_postcode'].label = _('우편번호')
		self.fields['buyer_postcode'].widget.attrs['readonly'] = True
		self.fields['buyer_postcode'].widget.attrs['placeholder'] = _('우편번호')
		self.fields['buyer_postcode'].widget.attrs.update({'id': 'id_postcode'})

		self.fields['buyer_addr'].label = _('주소')
		self.fields['buyer_addr'].widget.attrs['readonly'] = True
		self.fields['buyer_addr'].widget.attrs['placeholder'] = _('주소')
		self.fields['buyer_addr'].widget.attrs.update({'id': 'id_address'})

		self.fields['detail_addr'].label = _('상세주소')
		self.fields['detail_addr'].widget.attrs['placeholder'] = _('상세주소')
		self.fields['detail_addr'].widget.attrs.update({'id': 'id_detail_address'})

		self.fields['buyer_email'].label = _('이메일')
		self.fields['buyer_email'].widget.attrs['placeholder'] = _('이메일')

		self.fields['buyer_tel'].label = _('휴대전화')
		self.fields['buyer_tel'].widget.attrs['placeholder'] = _('휴대전화')

	def save(self, commit=True):
		order = super().save(commit=False)
		order.update(commit=commit)
		return order