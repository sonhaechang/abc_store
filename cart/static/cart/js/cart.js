class Cart {
    constructor() {
        this.url = document.getElementById('cart-js').getAttribute('add-cart-url');
        this.cart_list_url = document.getElementById('cart-js').getAttribute('cart-list-url');
        this.data = new FormData();

        axios.defaults.xsrfCookieName = 'csrftoken';
	    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    }

    create_success() {
        const result = confirm('장바구니에 상품이 추가 되었습니다. 장바구니를 확인하시겠습니까?');
        if (result) {
            location.href = this.cart_list_url;
        }
    }

    update_success() {

    }

    async axios_api(success_type) {
        try {
			const response = await axios.post(this.url, this.data);
	
			if (success_type == 'create') {
                this.create_success();
            } else {
                this.update_success();
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

    update_quantity() {
        this.data.append('item_id', item_id);
        this.data.append('quantity', quantity);
        this.axios_api('update');
    }
}