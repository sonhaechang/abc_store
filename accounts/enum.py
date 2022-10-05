from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class GenderEnum(TextChoices):
    """ 성별 열거 클래스 """
    MALE = 'MALE', _('남자')
    FEMALE = 'FEMALE', _('여자')