class Order {
	constructor() {
		this.cart_total_amount = 0;
		this.items = new Array();
	}

	mapped(ele) {
		const mapped = _.map(ele, item => {
			const item_id = item.getAttribute('data-item-id');
			const quantity = 1;
			return { item_id: item_id, quantity: quantity };
		});

		return mapped;
	}

 	filtered(mapped) {
		const filtered = _.filter(mapped, item => {
			return item.quantity > 0;
		});

		return filtered;
	}

	check_quantity(e, filtered) {
		if (filtered.length > 0) {
			const args = new URLSearchParams(_.object(_.map(filtered, _.values)));
			const url = e.currentTarget.getAttribute('href') + '?' + args;
			e.currentTarget.setAttribute('href', url);
			return true;
		}
		else {
			alert('1개 이상의 상품을 선택해주세요.');
		}
	
		return false;
	}

	calculate_total_amount() {
		document.getElementById('cart-total').innerText = this.comma(this.cart_total_amount);
	}

	select_items(checkboxs) {
		checkboxs.forEach(ele => {
            ele.addEventListener('change', e => {
				const item = e.target.parentNode.parentNode.parentNode;
				const amount = parseInt(document.getElementById(
					`total-amount-${e.target.getAttribute('data-id')}`).getAttribute('value'));

				if (e.target.checked) {
					this.cart_total_amount += amount;
					this.calculate_total_amount();
					this.items.push(item);
				} else {
					this.cart_total_amount -= amount;
					this.calculate_total_amount();
					this.items.splice(this.items.indexOf(item), 1);
				}				
            })
        })
		
	}

	order_new(e) {
		const mapped = this.mapped(this.items);
		const filtered = this.filtered(mapped);
		return this.check_quantity(e, filtered);
	}
}

Object.assign(Order.prototype, commaMixin);

// document.getElementById('order-new').addEventListener('click', e => {
// 	const mapped = _.map(document.querySelectorAll('#item-list .item'), item => {
// 		const item_id = item.getAttribute('data-item-id');
// 		const quantity = 1;
// 		return { item_id: item_id, quantity: quantity };
// 	});

// 	var filtered = _.filter(mapped, item => {
// 		return item.quantity > 0;
// 	});

// 	if ( filtered.length > 0) {
// 		const args = new URLSearchParams(_.object(_.map(filtered, _.values)));
// 		const url = e.currentTarget.getAttribute('href') + '?' + args;
// 		e.currentTarget.setAttribute('href', url);
// 		return true;
// 	}
// 	else {
// 		alert('상품 수량을 선택해주세요.');
// 	}

// 	return false;
// });