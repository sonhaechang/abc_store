from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from accounts.enums import GenderEnum

User = get_user_model()


class LoginForm(AuthenticationForm):
	''' 로그인시 사용하는 form '''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.error_messages['invalid_login'] = _('아이디 또는 비밀번호가 올바르지 않습니다.')


class SignupForm(UserCreationForm):
	''' 회원가입시 사용하는 form '''

	class Meta(UserCreationForm.Meta):
		model = User
		fields = UserCreationForm.Meta.fields + (
			'last_name', 'first_name', 'email', 'phone', 'gender',
			'postal_code', 'address', 'detail_address',
		)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		class_update_fields = {
			'username': _('아이디'), 'password1': _('비밀번호'), 'password2': _('비밀번호 확인'), 
			'last_name': _('성'), 'first_name': _('이름'), 'email': _('이메일'), 'phone': _('휴대전화'),
			'gender': _('성별'), 'postal_code': _('우편번호'), 'address': _('주소'), 'detail_address': _('상세주소')
		}
		
		for field_name in list(class_update_fields.keys()):
			self.fields[field_name].label = class_update_fields[field_name]
			self.fields[field_name].widget.attrs.update({
				'class': 'form-control',
				'placeholder': class_update_fields[field_name]
			})

		self.fields['address'].widget.attrs['readonly'] = True
		self.fields['postal_code'].widget.attrs['readonly'] = True
		self.fields['postal_code'].widget.attrs.update({'id': 'id_postcode'})
		self.fields['gender'] = forms.ChoiceField(
			widget=forms.RadioSelect({'class': 'd-flex'}),
			label=class_update_fields['gender'], 
			choices=GenderEnum.choices, 
			required=True)


class ProfileEditForm(forms.ModelForm):
	''' 프로필 수정할때 사용하는 form '''

	class Meta:
		model = User
		fields = ['last_name', 'first_name', 'email', 'phone', 'gender',
			'postal_code', 'address', 'detail_address']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		class_update_fields = { 
			'last_name': _('성'), 'first_name': _('이름'), 'email': _('이메일'), 'phone': _('휴대전화'),
			'gender': _('성별'), 'postal_code': _('우편번호'), 'address': _('주소'), 'detail_address': _('상세주소')
		}

		for field_name in list( class_update_fields.keys()):
			self.fields[field_name].label =  class_update_fields[field_name]
			self.fields[field_name].widget.attrs.update({
				'class': 'form-control',
				'placeholder':  class_update_fields[field_name],
			})

		self.fields['address'].widget.attrs['readonly'] = True
		self.fields['postal_code'].widget.attrs['readonly'] = True
		self.fields['postal_code'].widget.attrs.update({'id': 'id_postcode'})
		self.fields['email'].help_text = _('비밀번호 분실시 필요하니 정확히 입력해주세요.')
		self.fields['gender'] = forms.ChoiceField(
			widget=forms.RadioSelect({'class': 'd-flex'}),
			label=class_update_fields['gender'], 
			choices=GenderEnum.choices, 
			required=True)


class ProfileDetailForm(ProfileEditForm):
    ''' 프로필 확인할때 사용하는 form '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'disabled': 'True'})