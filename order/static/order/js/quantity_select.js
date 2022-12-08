class QuantitySelecter {
    constructor(factor_btn) {
        this.factor_btn = factor_btn;
    }

    quantity_select(is_update=false) {
        this.factor_btn.forEach(ele => {
            ele.addEventListener('click', e => {
                const id = e.currentTarget.getAttribute('data-id'),
                    el = e.currentTarget.parentNode.children[1],
                    factor = parseInt(e.currentTarget.getAttribute('data-factor')),
                    amount = e.currentTarget.getAttribute('value');
                const totalAmount = document.getElementById(`total-amount-${id}`)
                const quantity = parseInt(el.innerHTML) + factor;
                const total = amount * quantity;

                totalAmount.innerHTML = this.comma(total);
                totalAmount.setAttribute('value', total);

                if (quantity < 1 ) { quantity = 1; }
				el.innerHTML = quantity;

                if (is_update === true) {
                    cart.update_quantity(id, quantity);
                }
            })
        })
    }
}

Object.assign(QuantitySelecter.prototype, commaMixin);