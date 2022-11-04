def item_count(categorys):
	item_count = 0

	for category in categorys:
		item_count += category.item_category.all().count()
		
	return item_count