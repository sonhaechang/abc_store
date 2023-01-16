class Option {
    constructor() {
        this.optionObject = JSON.parse(
            document.getElementById('options-object-js').textContent);
        this.keys = Object.keys(this.optionObject);
        this.values = Object.values(this.optionObject);
        this.itemRealObject = new Object();
    }

    itemRealHandler() {
        const name = Object.values(this.itemRealObject).join('/');
        const itemReal = document.querySelectorAll('.item-real .item-real-name');

        itemReal.forEach(e => {
            if (e.innerText.trim() === name) {
                const id = e.getAttribute('data-id');
                document.getElementById(`item-real-${id}`).classList.remove('d-none');
                return false;
            }
        });
    }

    itemRealDelete() {
        document.querySelectorAll('.item-real-delete-btn').forEach(ele => {
            ele.addEventListener('click', e => {
                const id = e.target.getAttribute('value');
                document.getElementById(`item-real-${id}`).classList.add('d-none');
            })
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

const option = new Option();

option.selectOptions();
option.itemRealDelete();