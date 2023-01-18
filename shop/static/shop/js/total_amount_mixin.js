const totalAmountMixin = {
    get_total_amount_ele() {
        return document.getElementById('total-amount');
    },

    plus_total_amount(amount) {
        const totalAmount = this.get_total_amount_ele();
        const reusltAmount = parseInt(amount) + parseInt(totalAmount.getAttribute('value'));

        totalAmount.innerText = this.comma(reusltAmount);
        totalAmount.setAttribute('value', reusltAmount);
    },

    minus_total_amount(amount, setZero=false) {
        const totalAmount = this.get_total_amount_ele();
        let reusltAmount = parseInt(totalAmount.getAttribute('value')) - parseInt(amount);
        let defaultAmount = 0;

        document.querySelectorAll('#item-list .d-block').forEach(e => {
            defaultAmount = defaultAmount + parseInt(
                e.querySelector('.item-real-amount').innerText.trim());
        });

        if (!(setZero)) { 
            reusltAmount = (reusltAmount <= 0 || reusltAmount <= defaultAmount) ? 
                defaultAmount : reusltAmount; 
        }
        
        totalAmount.innerText = this.comma(reusltAmount);
        totalAmount.setAttribute('value', reusltAmount);
    }
}