from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class UserSession(TimeStampedModel):
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


	class Meta:
		db_table = 'user_session_tb'
		verbose_name = _('사용자 세션')
		verbose_name_plural = _('사용자 세션')