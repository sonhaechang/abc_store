from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from accounts.models import User, ShippingAddress
from dateutil.relativedelta import relativedelta


# Register your models here.
class UserDateJoinedFilter(admin.SimpleListFilter):
    title = '유저 가입일'
    parameter_name = 'date_joined'

    def lookups(self, reuqest, model_admin):
        candidate = []
        start_date = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        for i in range(6):
            value = f'{start_date.year}-{start_date.month}'
            label = f'{start_date.year}년 {start_date.month}월 가입자'
            candidate.append([value, label])
            start_date -= relativedelta(months=1)

        return candidate

    def queryset(self, request, queryset):
        value = self.value()

        if not value:
            return queryset

        try:
            year, month = map(int, value.split('-'))
            queryset = queryset.filter(date_joined__year=year, date_joined__month=month)
        except ValueError:
            return queryset.none()

        return queryset


class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    raw_id_fields = ['user']
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	fieldsets = BaseUserAdmin.fieldsets + (
		('추가 정보', {'fields': (
			'uuid', 'gender', 'birthdate', 'phone', 'profile_image',
			'postal_code', 'address', 'detail_address',
			'last_login_ip', 'sign_up_ip',
			'terms_of_service_is_agreed', 'terms_of_service_agreed_at',
			'personal_info_is_agreed', 'personal_info_agreed_at', 'marketing_is_agreed',
			'marketing_agreed_at', 'password_changed_at', 'password_fail_count', 
			'is_sign_out', 'sign_out_date', 'updated_at',
		)}),
	)

	add_fieldsets = BaseUserAdmin.add_fieldsets + (
		('추가 정보', {
			'fields': (
				'uuid', 'gender', 'birthdate', 'phone', 'profile_image',
				'postal_code', 'address', 'detail_address',
				'last_login_ip', 'sign_up_ip',
				'terms_of_service_is_agreed', 'terms_of_service_agreed_at',
				'personal_info_is_agreed', 'personal_info_agreed_at', 'marketing_is_agreed',
				'marketing_agreed_at', 'password_changed_at', 'password_fail_count', 
				'is_sign_out', 'sign_out_date', 'updated_at',
			),
		}),
	)

	readonly_fields = ('uuid', 'last_login', 'last_login_ip', 'sign_up_ip', 'updated_at',)
	list_display = [
		'username', 'last_name', 'first_name', 'email', 'phone', 
		'birthdate', 'gender', 'is_staff', 'is_sign_out']
	list_filter = ['is_staff', 'is_superuser', 'is_active', 'is_sign_out', UserDateJoinedFilter]
	inlines = [ShippingAddressInline]

	def get_search_results(self, request, queryset, search_term):
		''' 
			get_search_results override 
			get_search_results는 admin에서 search_fields 검색 기능 
			fullname으로 이름 검색 가능하게 필터링
		'''

		queryset, may_have_duplicates = super().get_search_results(
			request, queryset, search_term,
		)

		# 이름 검색시 icontains로 성과 이름 합쳐서 fullname을 filtering
		queryset |= self.model.objects.annotate(full_name=Concat('last_name', V(''), 'first_name')).filter(   
			Q(full_name__icontains=search_term) | 
			Q(first_name__icontains=search_term) | 
			Q(last_name__icontains=search_term)
		)

		return queryset, may_have_duplicates
