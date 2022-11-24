from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
	''' 로그인시 사용하는 form '''

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.error_messages['invalid_login'] = _('아이디 또는 비밀번호가 올바르지 않습니다.')
