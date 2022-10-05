from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

def validate_phone_length(value):
	raise RegexValidator(r'^010[1-9]\d{7}$', '-없이 11자 입력해주세요.')