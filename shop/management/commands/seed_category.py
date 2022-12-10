from django.core.management.base import BaseCommand

from faker import Faker
from django_seed import Seed

from shop.models import Category


class Command(BaseCommand):
	model_name = f'{Category}'
	help = f'이 명령은 {Category}를 만듭니다'

	def create_category_detail(self, category, category_details):
		for detail in category_details:
			Category.objects.create(
				category=category,
				name=detail,
				slug=detail
			)

	def handle(self, *args, **options):
		seeder = Seed.seeder()
		fake = Faker(['ko_KR'])
		
		categorys = ['가공식품', '신선식품']
		category_details_1 = ['통조림', '식용유', '소시지', '치즈', '초콜릿', '캔디']
		category_details_2 = ['육류', '생선', '채소']

		for category in categorys:
			cate = Category.objects.create(
				name=category,
				slug=category
			)

			if category == '가공식품':
				self.create_category_detail(cate, category_details_1)
			else:
				self.create_category_detail(cate, category_details_2)

		self.stdout.write(self.style.SUCCESS(f'{len(categorys)} {self.model_name} 생성!'))