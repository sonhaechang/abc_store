document.getElementById('order-new').addEventListener('click', e => {
	const mapped = _.map(document.querySelectorAll('#item-list .item'), item => {
		const item_id = item.getAttribute('data-item-id');
		const quantity = 1;
		return { item_id: item_id, quantity: quantity };
	});

	var filtered = _.filter(mapped, item => {
		return item.quantity > 0;
	});

	if ( filtered.length > 0) {
		const args = new URLSearchParams(_.object(_.map(filtered, _.values)));
		const url = e.currentTarget.getAttribute('href') + '?' + args;
		e.currentTarget.setAttribute('href', url);
		return true;
	}
	else {
		alert('상품 수량을 선택해주세요.');
	}

	return false;
});