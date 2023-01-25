class Order {
	constructor() {
		this.cart_total_amount = 0;
		this.carts = new Array();
		this.cart_ids = new Array();

		axios.defaults.xsrfCookieName = 'csrftoken';
		axios.defaults.xsrfHeaderName = 'X-CSRFToken';
	}

	calculate_total_amount() {
		document.getElementById('cart-total').innerText = this.comma(this.cart_total_amount);
	}

	select_items(checkboxs) {
		checkboxs.forEach(ele => {
            ele.addEventListener('change', e => {
				const cart = e.target.parentNode.parentNode.parentNode;
				const cart_id = cart.getAttribute('data-id');
				const amount = parseInt(document.getElementById(
					`total-amount-${e.target.getAttribute('data-id')}`).getAttribute('value'));

				if (e.target.checked) {
					this.cart_total_amount += amount;
					this.calculate_total_amount();
					this.carts.push(cart);
					this.cart_ids.push(cart_id);
				} else {
					this.cart_total_amount -= amount;
					this.calculate_total_amount();
					this.carts.splice(this.carts.indexOf(cart), 1);
					this.cartIds.splice(this.cart_ids.indexOf(cart_id), 1);
				}				
            })
        })
	}

	order_new(e) {
		e.preventDefault();

		const data = new FormData();
		data.append('cart_ids', JSON.stringify(this.cart_ids));

		if (this.carts.length > 0) {
			axios.post(e.target.href, data)
			.then(function (response) {
				location.href = response.data.redirect_url;
			})
			.catch(function (err) {
				console.error(err);
			})
		}
		else {
			alert('1개 이상의 상품을 선택해주세요.');
		}
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