class QuantitySelecter {
    constructor(factor_btn) {
        this.factor_btn = factor_btn;
    }

    comma(str) {
        str = String(str);
        return str.replace(/(\d)(?=(?:\d{3})+(?!\d))/g, '$1,');
    }

    uncomma(str) {
        str = String(str);
        return str.replace(/[^\d]+/g, '');
    }

    quantity_select() {
        console.log(this.factor_btn);
        this.factor_btn.forEach(ele => {
            ele.addEventListener('click', e => {
                const totalAmount = document.querySelector('.total-amount'),
                    el = e.currentTarget.parentNode.children[1],
                    factor = parseInt(e.currentTarget.getAttribute('data-factor')),
                    amount = e.currentTarget.getAttribute('value');
        
                const quantity = parseInt(el.innerHTML) + factor;
                const total = this.comma(amount * quantity);

                totalAmount.innerHTML = total;

                if (quantity < 1 ) { quantity = 1; }
				el.innerHTML = quantity;
            })
        })
    }
}

