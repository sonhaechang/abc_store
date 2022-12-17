
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from order.models import Order, OrderItem
from order.services import OrderItemHandler, export_excel


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
