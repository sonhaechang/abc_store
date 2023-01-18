class QuantitySelecter {
    constructor(factor_btn) {
        this.factor_btn = factor_btn;
    }

    quantity_select(is_update=false) {
        this.factor_btn.forEach(ele => {
            ele.addEventListener('click', e => {
                const id = e.currentTarget.getAttribute('data-id');
                const cartId = e.currentTarget.getAttribute('data-cart-id');
                const totalAmount = document.getElementById(`total-amount-${id}`) ? 
                    document.getElementById(`total-amount-${id}`) : 
                    document.getElementById(`total-amount-${cartId}`);

                const el = e.currentTarget.parentNode.children[1],
                    factor = parseInt(e.currentTarget.getAttribute('data-factor')),
                    amount = e.currentTarget.getAttribute('value');
                
                let quantity = parseInt(el.innerHTML) + factor;

                if (quantity < 1 ) { quantity = 1; }
				el.innerHTML = quantity;

                const total = amount * quantity;
                
                totalAmount.innerHTML = this.comma(total);
                totalAmount.setAttribute('value', total);

                if (is_update === true) {
                    cart.update_quantity(e, factor);
                } else {
                    if (factor === 1) {
                        this.plus_total_amount(amount);
                    } else {
                        this.minus_total_amount(amount);
                    }
                }
            })
        })
    }
}

Object.assign(QuantitySelecter.prototype, commaMixin, totalAmountMixin);