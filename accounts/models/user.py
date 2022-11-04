import os
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.enums import GenderEnum
from accounts.validators import validate_phone_length

from core.managers import CustomUserManager


# Create your models here.
def profile_upload_to(instance, filename):
	ymd_path = timezone.now().strftime('%Y%m%d')
	_uuid = instance.uuid
	filename_base, filename_ext = os.path.splitext(filename) # 확장자 추출
	# return f'users/{_uuid}/profile/profile_{filename_base}_{ymd_path}{filename_ext}'
	return f'users/{_uuid}/profile/profile_{ymd_path}'


class User(AbstractUser):
	''' 사용자 모델 '''

	uuid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
		verbose_name=_('고유식별자')
    )

	gender = models.CharField(
        max_length=9,
        choices=GenderEnum.choices,
        default=GenderEnum.MALE,
		verbose_name=_('성별'),
		help_text=_('성별입니다. 남, 여')
    )

	birthdate = models.CharField(
        max_length=8,
        blank=True,
        null=True,
		verbose_name=_('생년월일'),
		help_text=_('생년월일 8자리를 입력하세요.')
    )

	postal_code = models.CharField(
		blank=True, 
		max_length=20,
		verbose_name=_('우편번호')
	)

	address = models.CharField(
		blank=True, 
		max_length=100,
		verbose_name=_('주소')
	)

	detail_address = models.CharField(
		blank=True, 
		max_length=100,
		verbose_name=_('상세주소')
	)

	phone = models.CharField(
		blank=True, 
		max_length=11, 
		validators=[validate_phone_length],
		verbose_name=_('휴대폰'),
		help_text=_('- 를 제외한 번호만 입력하세요.'),
	)

	profile_image = models.ImageField(
        upload_to=profile_upload_to,
        blank=True,
        null=True,
		verbose_name=_('프로필 이미지')
    )

	last_login_ip = models.GenericIPAddressField(
    	editable=False,
        blank=True,
        null=True,
		verbose_name=_('마지막 로그인 IP'),
		help_text=_('최근 로그인된 IP 입니다.')
    )

	sign_up_ip = models.GenericIPAddressField(
		editable=False,
		blank=True,
		null=True,
		verbose_name=_('가입 IP'),
		help_text=_('가입한 IP 입니다.')
	)

	terms_of_service_is_agreed = models.BooleanField(
		blank=True,
		null=True,
		verbose_name=_('서비스 이용약관 동의 여부')
	)

	terms_of_service_agreed_at = models.DateTimeField(
		blank=True,
		null=True,
		verbose_name=_('서비스 이용약관 동의일')
	)

	personal_info_is_agreed = models.BooleanField(
		blank=True,
		null=True,
		verbose_name=_('개인정보 동의 여부')
	)

	personal_info_agreed_at = models.DateTimeField(
		blank=True,
		null=True,
		verbose_name=_('개인정보 동의일')
	)

	marketing_is_agreed = models.BooleanField(
		blank=True,
		null=True,
		default=False,
		verbose_name=_('마케팅 수신 동의 여부')
	)

	marketing_agreed_at = models.DateTimeField(
		blank=True,
		null=True,
		verbose_name=_('마케팅 수신 동의일')
	)

	password_changed_at = models.DateTimeField(
		blank=True,
		null=True,
		verbose_name=_('비밀번호 변경일')
	)

	password_fail_count = models.SmallIntegerField(
		blank=True,
		null=True,
		verbose_name=_('비밀번호 실패 횟수')
	)

	is_sign_out = models.BooleanField(
		blank=True,
		default=False,
		verbose_name=_('회원탈퇴 여부')
	)

	sign_out_date = models.DateTimeField(
		blank=True,
		null=True,
		verbose_name=_('회원탈퇴일')
	)

	updated_at = models.DateTimeField(
		auto_now=True,
		editable=False,
		blank=True,
		null=True,
		verbose_name=_('수정일'),
		help_text=_('사용자 정보 수정일입니다.')
	)

	objects = CustomUserManager()


	class Meta:
		db_table = 'users_tb'
		verbose_name = _('사용자')
		verbose_name_plural = _('사용자')