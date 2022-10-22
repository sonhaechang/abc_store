from django.contrib import admin
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from shop.models import Category, CategoryDetail, Item, ItemImage, Review

# Register your models here.
class ReviewDateCreatedFilter(admin.SimpleListFilter):
    title = '리뷰 작성일'
    parameter_name = 'created_at'

    def lookups(self, reuqest, model_admin):
        candidate = []
        start_date = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        for i in range(6):
            value = f'{start_date.year}-{start_date.month}'
            label = f'{start_date.year}년 {start_date.month}월 작성'
            candidate.append([value, label])
            start_date -= relativedelta(months=1)

        return candidate

    def queryset(self, request, queryset):
        value = self.value()

        if not value:
            return queryset

        try:
            year, month = map(int, value.split('-'))
            queryset = queryset.filter(created__year=year, created__month=month)
        except ValueError:
            return queryset.none()

        return queryset


class ItemImageInline(admin.StackedInline):
    model = ItemImage
    raw_id_fields = ['item']
    extra = 1


class ReviewInline(admin.StackedInline):
	model = Review
	raw_id_fields = ['item']
	extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'created_at', 'updated_at']
	list_display_links = ['id', 'name']
	search_fields = ['name']
	prepopulated_fields = {'slug':('name',)}


@admin.register(CategoryDetail)
class CategoryDetailAdmin(admin.ModelAdmin):
	list_display = ['id', 'category', 'name', 'created_at', 'updated_at']
	list_display_links = ['id', 'name']
	search_fields = ['name']
	prepopulated_fields = {'slug':('name',)}


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	list_display = ['id', 'category', 'name', 'stock', 'is_public']
	list_display_links = ['id', 'name']
	list_filter = ['category']
	list_editable = ['is_public', 'stock']
	search_fields = ['name']
	inlines = [ItemImageInline, ReviewInline]
	prepopulated_fields = {'slug':('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'created_at']
	list_filter = ['rating', ReviewDateCreatedFilter]
	search_fields = ['user']