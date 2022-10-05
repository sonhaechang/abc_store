from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserSession(models.Model):
	''' 사용자 세션 모델 '''

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE, 
		editable=False,
		verbose_name=_('사용자')
	)

	session_key = models.CharField(
		max_length=40,
		editable=False,
		verbose_name=_('세션 키')
	)

	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name=_('생성일')
	)
	
	updated_at = models.DateTimeField(
		auto_now=True,
		verbose_name=_('수정일')
	)