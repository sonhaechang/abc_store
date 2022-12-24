from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from dateutil.relativedelta import relativedelta

from shop.models import Category, Item, ItemOption, ItemReal, ItemImage, Review

# Register your models here.
class ReviewDateCreatedFilter(admin.SimpleListFilter):
    title = _('리뷰 작성일')
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


class CategoryFilter(admin.SimpleListFilter):
    title = _('메인 카테고리')
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        categorys = set([category.category for category in model_admin.model.objects.exclude(category=None)])
        return [(category.pk, category.name) for category in categorys]

    def queryset(self, request, queryset):
        return queryset.filter(category__pk__exact=self.value())


class ItemImageInline(admin.StackedInline):
    model = ItemImage
    raw_id_fields = ['item']
    extra = 0


class ReviewInline(admin.StackedInline):
	model = Review
	raw_id_fields = ['item']
	extra = 0


class ItemRealInline(admin.StackedInline):
    model = ItemReal
    raw_id_fields = ['item'] 
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    list_filter = [CategoryFilter]
    search_fields = ['name']
    prepopulated_fields = {'slug':('name',)}


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    raw_id_fields = ['category']
    list_display = ['id', 'category', 'name', 'is_public']
    list_display_links = ['id', 'name']
    list_filter = ['category']
    list_editable = ['is_public']
    search_fields = ['name']
    inlines = [ItemRealInline, ItemImageInline]
    prepopulated_fields = {'slug':('name',)}


@admin.register(ItemOption)
class ItemOptionAdmin(admin.ModelAdmin):
    raw_id_fields = ['item']
    list_display = ['id', 'name', 'value']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'created_at']
	list_filter = ['rating', ReviewDateCreatedFilter]
	search_fields = ['user']