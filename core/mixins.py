from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import ContextMixin

class PaginationsMixins(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		page = self.request.GET.get('page', 1)
		obj = self.get_queryset()

		total_len = len(obj)
		paginator = Paginator(obj, int(10))
		try:
			obj = paginator.page(page)
		except PageNotAnInteger:
			obj = paginator.page(1)
		except EmptyPage:
			obj = paginator.page(paginator.num_pages)

		index = obj.number -1
		max_index = len(paginator.page_range)
		start_index = index - 2 if index >= 2 else 0

		if index < 2 :
			end_index = 5 - start_index
		else :
			end_index = index + 3 if index <= max_index - 3 else max_index

		page_range = list(paginator.page_range[start_index:end_index])

		context['obj_list'] = obj
		context['total_len'] = total_len
		context['page_range'] = page_range
		context['max_index'] = max_index - 2

		return context