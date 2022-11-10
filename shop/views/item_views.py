from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from core.mixins import PaginationsMixins

from shop.models import Category, CategoryDetail, Item
from shop.services import item_count

# Create your views here.
class CategoryListAllView(PaginationsMixins, ListView):
	template_name = 'shop/container/category_list_all.html'

	def get_object(self, **kwargs):
		return Category.objects.get_or_none(slug=self.kwargs['category_slug'])

	def get_categorys(self, **kwargs):
		category = self.get_object()

		if category is not None:
			return category.categorydetail_category.all(
				).order_by('created_at').prefetch_related('item_category')
		else:
			return list()

	def get_queryset(self, **kwargs):
		return [item for category in self.get_categorys() for item in Item.objects.filter(
			category=category).select_related('category').prefetch_related('itemimage_item')]
		
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['category'] = self.get_object()
		context['categorys'] = self.get_categorys()
		context['item_count'] = item_count(context['categorys'])

		return context


class CategoryListView(PaginationsMixins, ListView):
	model = CategoryDetail
	template_name = 'shop/container/category_list.html'

	def get_object(self, **kwargs):
		return get_object_or_404(
			self.model.objects.select_related('category'), 
			slug=self.kwargs['sub_category_slug'])

	def get_queryset(self, **kwargs):
		return [category for category in \
			self.get_object().item_category.all().order_by('-id').prefetch_related('itemimage_item')]

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		category = self.get_object()
		categorys = self.model.objects.prefetch_related(
			'item_category').select_related('category').filter(category__pk=category.category.pk)

		context['category'] = category
		context['categorys'] = categorys
		context['item_count'] = item_count(categorys)
		context['item_quantity'] = len(self.get_queryset())

		return context


def item_detail(request, category_slug, sub_category_slug, item_slug):
	item = get_object_or_404(
		Item.objects.prefetch_related('review_item', 'itemimage_item'), slug=item_slug)

	review_url = reverse('shop:review', kwargs={'item_pk': item.pk})

	# TODO: sklearn을 이용한 recommendation system model을 학습을 시켜서 추천하는 것으로 변경 필요
	related_items = Item.objects.filter(
		category=item.category).select_related('category').prefetch_related('photo_set')

	context = {
		'item': item,
		'review_url': review_url,
		'related_items': related_items
	}

	return render(request, 'shop/container/item_detail.html', context)