from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
		verbose_name=_('생성일'),
        help_text=_('데이터가 생성된 일자입니다.'),
    )

	updated_at = models.DateTimeField(
		auto_now=True,
		editable=False,
		verbose_name=_('수정일'),
		help_text=_('데이터가 수정된 사용자입니다.'),
	)

	class Meta:
		abstract = True


# 모든 모델에 들어갈 공통 필드, 설정
class HistoryModel(TimeStampedModel):
	is_deleted = models.BooleanField(
		editable=False,
		default=False,
		blank=True,
		verbose_name=_('삭제 여부'),
		help_text=_('데이터 삭제 여부입니다.'),
	)

	deleted_at = models.DateTimeField(
		editable=False,
		blank=True,
		null=True,
		verbose_name=_('삭제일'),
		help_text=_('데이터를 삭제한 일자입니다.'),
	)

	class Meta:
		abstract = True
