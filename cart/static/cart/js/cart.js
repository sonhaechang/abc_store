class Cart {
    constructor() {
        this.url = document.getElementById('cart-js').getAttribute('add-cart-url');
        this.cart_list_url = document.getElementById('cart-js').getAttribute('cart-list-url');
        this.data = new FormData();

        axios.defaults.xsrfCookieName = 'csrftoken';
	    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    }

    set_total_amount() {
        const carts = document.querySelectorAll('.cart-table .cart');
        
        if (carts.length === 0) {
            document.querySelector('.cart-table').remove();
            document.getElementById('cart-total-wrap').remove();
            document.getElementById('cart-content').innerHTML = '<p>장바구니에 담긴 상품이 없습니다.</p>';
        }
    }

    create_success() {
        const result = confirm('장바구니에 상품이 추가 되었습니다. 장바구니를 확인하시겠습니까?');
        if (result) {
            location.href = this.cart_list_url;
        }
    }

    delete_success(target, message) {
        alert(message);
        document.getElementById(`cart-${target.getAttribute('data-id')}`).remove();
        this.set_total_amount();
    }

    async axios_api(success_type, delete_target=null) {
        const url = delete_target != null ? delete_target.getAttribute('href') : this.url;

        try {
			const response = await axios.post(url, this.data);
	
			if (success_type == 'create') {
                this.create_success();
            } else if (success_type == 'delete') {
                this.delete_success(delete_target, response.data.message);
            }
		} catch(err) {
			console.error(err);
		}
    }

    add_cart(ele) {
        const items = this.create_item_real_objects(ele);

        if (Object.keys(items).length <= 0) {
            alert('상품 옵션을 선택해주세요.');
            return false;
        }
                
        this.data.append('item_reals', JSON.stringify(items));
        this.axios_api('create');
    }

    update_quantity(ele, quantity) {
        const id = ele.target.getAttribute('data-cart-id');
        const itemEle = document.querySelectorAll(`#cart-${id}`);
        const item = this.create_item_real_objects(itemEle, quantity);

        this.data.append('item_reals', JSON.stringify(item));
        this.axios_api('update');
    }

    delete_cart(event) {
        event.preventDefault();
        this.axios_api('delete', event.target);
    }
}

Object.assign(Cart.prototype, commaMixin, ItemRealMixin);