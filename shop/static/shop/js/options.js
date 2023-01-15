class Option {
    constructor() {
        this.optionObject = JSON.parse(
            document.getElementById('options-object-js').textContent);
        this.itemRealEle = document.querySelectorAll('.item_real .item_real_name');
        this.itemRealObject = new Object();
        this.keys = Object.keys(this.optionObject);
        this.values = Object.values(this.optionObject);
    }

    itemRealHandler() {
        const name = Object.values(this.itemRealObject).join('/');

        this.itemRealEle.forEach(e => {
            if (e.innerText.trim() === name) {
                const id = e.getAttribute('data-id');
                document.getElementById(`item_real_${id}`).classList.remove('d-none');
                return false;
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
            const selectBox = document.getElementById(`select_option_box_${idx}`);

            selectBox.addEventListener('change', () => {
                const option = selectBox.options[selectBox.selectedIndex].value;

                this.itemRealObject[`select_option_box_${idx}`] = option;

                if (keyLen === idx) {
                    this.itemRealHandler();
                } else {
                    const nextSelectBox = document.getElementById(`select_option_box_${idx+1}`);

                    if (nextSelectBox) { this.makeOptions(nextSelectBox, this.keys[idx]); }
                }
            });
        });
    }
}
