class Option {
    constructor() {
        this.optionObject = JSON.parse(
            document.getElementById('options-object-js').textContent);

        this.keys = Object.keys(this.optionObject);
        this.values = Object.values(this.optionObject);
        this.itemRealObject = new Object();
    }

    resetAmountAndQuantity(itemEle, totalAmountEle) {
        const amount = itemEle.querySelector('.item-real-amount').innerText.trim();

        totalAmountEle.setAttribute('value', amount)
        totalAmountEle.innerText = this.comma(parseInt(amount));
        itemEle.querySelector('.quantity').innerText = 1;
    }

    itemRealToggle(ele, firstClass, secondCalss) {
        ele.classList.replace(firstClass, secondCalss);
    }

    itemRealHandler() {
        const name = Object.values(this.itemRealObject).join('/');
        const itemReal = document.querySelectorAll('.item-real .item-real-name');

        itemReal.forEach(e => {
            if (e.innerText.trim() === name) {
                const id = e.getAttribute('data-id');
                const amount = document.querySelector(`#item-real-${id} .factor-btn`).getAttribute('value');
                const itemEle = document.getElementById(`item-real-${id}`);

                this.itemRealToggle(itemEle, 'd-none', 'd-block');
                
                if (Array.from(itemEle.classList).includes('d-block')) {
                    this.plus_total_amount(amount); 
                }

                this.resetSelectOption();

                return false;
            }
        });
    }

    itemRealDelete() {
        document.querySelectorAll('.item-real-delete-btn').forEach(ele => {
            ele.addEventListener('click', e => {
                const id = e.target.getAttribute('value');
                const totalAmountEle = document.getElementById(`total-amount-${id}`);
                const itemEle = document.getElementById(`item-real-${id}`);

                this.itemRealToggle(itemEle, 'd-block', 'd-none');
                this.minus_total_amount(totalAmountEle.getAttribute('value'), true);
                this.resetAmountAndQuantity(itemEle, totalAmountEle);
            })
        });
    }

    resetSelectOption() {
        const selectBox = document.querySelectorAll('.select-option-box');
        selectBox[0].options[0].selected = true;

        selectBox.forEach((e, i) => {
            if (i !== 0) {
                e.innerHTML = `<option value="">옵션을 선택해주세요.</option>`;
            }
        });
    }

    makeOptions(selectBox, key) {
        selectBox.innerHTML = `<option value="">옵션을 선택해주세요.</option>`;

        this.optionObject[key].forEach(e => {
            selectBox.innerHTML += `<option value='${e}'>${e}</option>`;
        })
    }

    selectOptions() {
        this.keys.forEach((key, idx) => {
            idx = idx + 1;
            const keyLen = this.keys.length;
            const selectBox = document.getElementById(`select-option-box-${idx}`);

            selectBox.addEventListener('change', () => {
                const option = selectBox.options[selectBox.selectedIndex].value;

                this.itemRealObject[`select-option-box-${idx}`] = option;

                if (keyLen === idx) {
                    this.itemRealHandler();
                } else {
                    const nextSelectBox = document.getElementById(`select-option-box-${idx+1}`);

                    if (nextSelectBox) { this.makeOptions(nextSelectBox, this.keys[idx]); }
                }
            });
        });
    }
}

Object.assign(Option.prototype, commaMixin, totalAmountMixin);

const option = new Option();

option.selectOptions();
option.itemRealDelete();