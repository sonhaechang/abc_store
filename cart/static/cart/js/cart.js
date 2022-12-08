class Cart {
    constructor() {
        this.url = document.getElementById('cart-js').getAttribute('add-cart-url');
        this.cart_list_url = document.getElementById('cart-js').getAttribute('cart-list-url');
        this.data = new FormData();

        axios.defaults.xsrfCookieName = 'csrftoken';
	    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    }

    set_total_amount() {
        let total_amount = 0;
        const cart_total = document.getElementById('cart-total');

        document.querySelectorAll('.total-amount').forEach(e => {
            total_amount += parseInt(e.getAttribute('value'));
        });
        
        if (total_amount === 0) {
            document.getElementById('cart-table').remove();
            document.getElementById('cart-total-wrap').remove();
            document.getElementById('cart-content').innerHTML = '<p>장바구니에 담긴 상품이 없습니다.</p>';
        } else {
            cart_total.innerText = this.comma(total_amount);
        }
    }

    create_success() {
        const result = confirm('장바구니에 상품이 추가 되었습니다. 장바구니를 확인하시겠습니까?');
        if (result) {
            location.href = this.cart_list_url;
        }
    }

    update_success() {
        this.set_total_amount();
    }

    delete_success(target, message) {
        alert(message);
        document.getElementById(`item-${target.getAttribute('data-id')}`).remove();
        this.set_total_amount();
    }

    async axios_api(success_type, delete_target=null) {
        const url = delete_target != null ? delete_target.getAttribute('href') : this.url;

        try {
			const response = await axios.post(url, this.data);
	
			if (success_type == 'create') {
                this.create_success();
            } else if (success_type == 'update') {
                this.update_success();
            } else {
                this.delete_success(delete_target, response.data.message);
            }
		} catch(err) {
			console.error(err);
		}
    }

    add_cart(self, item_id, quantity) {
        self.data.append('item_id', item_id);
        self.data.append('quantity', quantity);
        self.axios_api('create');
    }

    update_quantity(item_id, quantity) {
        this.data.append('item_id', item_id);
        this.data.append('quantity', quantity);
        this.axios_api('update');
    }

    delete_cart(event) {
        event.preventDefault();
        this.axios_api('delete', event.target);
        
    }
}

Object.assign(Cart.prototype, commaMixin);