from shop.models import Category


def navbar_categorys(request):
	return {'navbar_categorys': Category.objects.filter(category__isnull=True)}