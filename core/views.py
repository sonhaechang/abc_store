from django.shortcuts import render

from shop.models import Item

# Create your views here.

def main(request):
	#TODO: 주석 처리된 부분 models 생성후 주석 해제해야됨

	best_item = Item.objects.filter(best_item=True)[:12]
    # carousel_list = Carousel.objects.all()
    # main_img_halal = MainImages.objects.first()
    # main_img_alcohol = MainImages.objects.last()

	return render(request, 'core/container/main.html', {
		'item': best_item,
        # 'carousel_list': carousel_list,
        # 'main_img_halal': main_img_halal,
        # 'main_img_alcohol': main_img_alcohol,
	})