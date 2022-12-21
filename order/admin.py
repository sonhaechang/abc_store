import openpyxl

from django.contrib import admin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.urls import path

from order.models import Order, OrderItem
from order.services import (
	OrderItemHandler, 
	export_excel, import_excel
)


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['item']
    fields = ['pk', 'item', 'quantity', 'status']
    readonly_fields = ('pk',)
    extra = 0

    def pk(self, orderitem):
        return orderitem.pk


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	change_list_template = 'admin/container/order_change_list.html'
	fields = ['user', 'merchant_uid', 'imp_uid', 'name', 'amount', 'delivery_amount', 'delivery_number', 
		'status', 'meta', 'buyer_name', 'buyer_postcode', 'buyer_addr', 'detail_addr', 'buyer_email', 
		'buyer_tel', 'exchange_return', 'vbank_num', 'created_at']
	readonly_fields = ('imp_uid', 'merchant_uid', 'status', 'name', 'vbank_num', 'delivery_amount', 'created_at',)
	list_display = ['merchant_uid', 'username', 'name', 'amount_html', 'status_html', 'created_at']
	# list_display_links = ['user']
	raw_id_fields = ['user']
	actions = ['do_update', 'do_cancel', 'do_export_excel']
	list_filter = ['created_at', 'status']
	search_fields = ['imp_uid', 'user__username', 'name']
	inlines = [OrderItemInline]

	# change_list_template = 'order/admin/order_list_form.html'

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		return qs.select_related('user')

	def username(self, obj):
		user_id = f'<span><small>({obj.user.username})</small></span>'
		user_name = f'<span>{obj.user.first_name}{obj.user.last_name}</span>'
		result = user_name + '<br/>' + user_id
		return mark_safe(result)
	username.short_description = '주문자'

	def do_update(self, request, queryset):
		'주문 정보를 갱신합니다.'
		total = queryset.count()
		if total > 0:
			for order in queryset:
				order.update()
			self.message_user(request, f'주문 {total} 건의 정보를 갱신했습니다.')
		else:
			self.message_user(request, '갱신할 주문이 없습니다.')
	do_update.short_description = '선택된 주문들의 아임포트 정보 갱신하기'

	def do_cancel(self, request, queryset):
		'선택된 주문에 대해 결제취소요청을 합니다.'
		queryset = queryset.filter(status='paid')
		total = queryset.count()
		if total > 0:
			for order in queryset:
				order.cancel()
				order_item_handler = OrderItemHandler(order)
				order_item_handler.set_cancel_status()
				order_item_handler.stock_plus_counter()
			self.message_user(request, f'주문 {total} 건을 취소했습니다.')
		else:
			self.message_user(request, '취소할 주문이 없습니다.')
	do_cancel.short_description = '선택된 주문에 대해 결제취소'

	def do_export_excel(self, request, queryset):
		'선택된 주문에 대해 엑셀로 다운로드를 합니다.'
		try:
			total = queryset.count()
			if total > 0:
				response = export_excel(queryset)
				self.message_user(request, f'{total} 건의 주문을 엑셀로 다운로드했습니다.')
				return response
			else:
				self.message_user(request, '취소할 주문이 없습니다.')
		except Exception as e:
			self.message_user(request, f'엑셀 다운로드에 실패 했습니다. 다시 시도해주세요.')
	do_export_excel.short_description = '선택된 주문에 대해 엑셀로 다운로드'

	def get_urls(self):
		''' custom admin urls '''

		urls = super().get_urls()
		order_urls = [
			path('import/excel/shipping-num/', 
				self.admin_site.admin_view(self.shipping_number_update_to_excel), 
				name="shipping_number_update_to_excel")
		]
		return order_urls + urls

	def shipping_number_update_to_excel(self, request):
		''' 입력받은 등기번호 엑셀파일 불러와서 등기번호 업데이트 '''

		if request.method == 'POST':
			import_excel(request.FILES['upload_file'].file)
			
			return redirect(
				f'admin:{self.model._meta.app_label}_{self.model._meta.model_name}_changelist')

		context = dict(
			self.admin_site.each_context(request),
			opts=self.model._meta
		)

		return TemplateResponse(request, 'admin/container/shipping_number_update_to_excel.html', context)