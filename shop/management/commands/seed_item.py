import random
import datetime

from django.core.management.base import BaseCommand

from faker import Faker
from django_seed import Seed

from shop.models import CategoryDetail, Item

class Command(BaseCommand):
	model_name = f'{Item}'
	help = f'이 명령은 {Item}를 만듭니다'

	def add_arguments(self, parser):
		parser.add_argument(
			'--number', 
			default=50, 
			type=int, 
			help=f'몇개의 {self.model_name}를 생성 하시겠습니까?'
		)

	def handle(self, *args, **options):
		number = options.get('number')
		seeder = Seed.seeder()
		fake = Faker(['ko_KR'])

		categorys = CategoryDetail.objects.all()

		is_sales = [1, 2]
		booleans = [True, False]
		description = '못할 힘차게 찾아 그들은 인생을 목숨이 피가 없는 더운지라 교향악이다. 만물은 힘차게 얼음에 교향악이다. 시들어 너의 얼마나 있는 위하여 현저하게 무한한 그리하였는가? 청춘이 열락의 피어나는 뿐이다.'

		for i in range(1, number+1):
			name = f'상품명{i}'
			amount = i * 1000
			sale_amount = amount / random.choice(is_sales)
			sale_percent = ((amount-sale_amount) / amount) * 100

			Item.objects.create(
				category=random.choice(categorys),
				name=name,
				slug=name,
				description=description,
				amount=amount,
				sale_percent=sale_percent,
				sale_amount=sale_amount,
				stock=100,
				is_halal=random.choice(booleans),
				is_public=True,
				best_item=random.choice(booleans)
			)

		self.stdout.write(self.style.SUCCESS(f'{number} {self.model_name} 생성!'))