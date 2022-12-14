class Option {
    constructor() {
        this.optionsInlineCount = 0;
        this. optionObject = new Object();
    }

    makeOptionBadge(data, id) {
        const badgeDeleteBtn = document.querySelectorAll(
            `#id_option_result_${id} .option-badge-delete`).length;

        return `
            <span class="option-badge">
                <span class="option-badge-text">
                    ${data}
                </span>
                <a href="#"
                    id="option_badge_delete_${id}_${badgeDeleteBtn+1}"
                    class="inline-deletelink option-badge-delete"
                    data-id="${id}">
                    삭제하기
                </a>
            </span>
        `
    }

    makeAddOptionEle() {
        const id = this.optionsInlineCount;
        return `
            <div id="inline_related_${id}" class="inline-related" data-id=${id}>
                <h3>
                    <b>옵션 품목:</b>
                    <span class="inline_label">#${id}</span>
                    <a href="#"
                        id="option_input_delete_${id}" 
                        class="inline-deletelink" 
                        data-id=${id}>
                        삭제하기
                    </a>
                </h3>

                <fieldset class="module aligned ">
                    <div class="option-input-inner" style="display: flex;">
                        <div class="form-row" style="flex-grow: 0;">
                            <input 
                                type="text" 
                                id="id_option_name_${id}"
                                class="class_option_name" 
                                placeholder="옵션명 입력"
                                data-id=${id}>
                        </div>
                        <div class="form-row" style="flex-grow: 2;">
                            <input 
                                type="text"
                                id="id_option_value_${id}" 
                                class="class_option_value" 
                                placeholder="옵션값 입력 - 엔터" 
                                style="width: 99.5%;"
                                data-id=${id}>
                        </div>
                    </div>
                    <div id="id_option_result_${id}" class="form-row option-result">
                    </div>
                </fieldset>
            </div>
        `
    }

    arrayProduct(...arrays) {
        return arrays[0].reduce((prevAccumulator, currentArray) => {
            let newAccumulator = new Array();

            prevAccumulator.forEach(prevAccumulatorArray => {
                currentArray.forEach(currentValue => {
                    newAccumulator.push(prevAccumulatorArray.concat(currentValue));
                });
            });

            return newAccumulator;
        }, [[]]);
    }

    setOptionAttr(elements) {
        elements.forEach(e => {
            const prevId = parseInt(e.getAttribute('data-id'));
            const currentId = prevId - 1;

            const inputDelet = e.querySelector('.inline-deletelink');
            const inputName = e.querySelector('.class_option_name');
            const inputValue = e.querySelector('.class_option_value');

            e.querySelector('.option-result').setAttribute('id', `id_option_result_${currentId}`);
            e.setAttribute('id', `inline_related_${currentId}`);
            e.setAttribute('data-id', `${currentId}`);
            e.querySelector('.inline_label').innerText = `${currentId}`;

            inputDelet.setAttribute('id', `option_input_delete_${currentId}`);
            inputDelet.setAttribute('data-id', `${currentId}`);

            inputName.setAttribute('id', `id_option_name_${currentId}`);
            inputName.setAttribute('data-id', `${currentId}`);

            inputValue.setAttribute('id', `id_option_value_${currentId}`);
            inputValue.setAttribute('data-id', `${currentId}`);

            this.setOptionBadgeAttr(currentId);
        });
    }

    setOptionBadgeAttr(parentId) {
        document.querySelectorAll(`#id_option_result_${parentId} .option-badge`).forEach(e => {
            const aTag = e.querySelector('.option-badge-delete');
            const id = aTag.getAttribute('id').slice(-1);

            aTag.setAttribute('id', `option_badge_delete_${parentId}_${id}`);
            aTag.setAttribute('data-id', parentId);
        })
    }

    optionRename(id) {
        const currentID = parseInt(id);
        const options = document.querySelectorAll('.options-input-block .inline-related');
        const lastID = parseInt(options[options.length-1].getAttribute('id').slice(-1));

        if (currentID < lastID) {
            this.setOptionAttr(Array.from(options).slice(currentID-1));
            this.optionNameHandler();
        }
    }

    optionNameHandler() {
        document.querySelectorAll('.class_option_name').forEach(ele => {
            ele.addEventListener('keydown', e => {
                if (e.keyCode === 13) {
                    e.preventDefault();
                };
            });
        });
    }

    optionValueHandler() {
        document.getElementById(`id_option_value_${this.optionsInlineCount}`).addEventListener('keydown', e => {
            if (e.keyCode === 13) {
                e.preventDefault();

                const valueInput = e.target;
                const id = e.target.getAttribute('data-id');
                const nameInput = document.getElementById(`id_option_name_${id}`);

                if (nameInput.value === '') {
                    alert('옵션명을 입력해주세요.');
                    return false; 
                }  

                if (valueInput.value === '') {
                    alert('옵션값을 입력해주세요.');
                    return false;
                }

                this.optionBadgeHandler(id, valueInput.value);
                valueInput.value = '';
            }; 
        });
    }

    optionBadgeHandler(id, value) {
        document.getElementById(`id_option_result_${id}`).insertAdjacentHTML(
            'beforeend', this.makeOptionBadge(value, id));

        const badgeDeleteBtn = document.querySelectorAll(
            `#id_option_result_${id} .option-badge-delete`).length;

        document.getElementById(
            `option_badge_delete_${id}_${badgeDeleteBtn}`).addEventListener('click', e => this.optionBadgeDelete(e));
    }

    addOption() {
        document.querySelector('.field-options .add-row').addEventListener('click', e => {
            e.preventDefault();
            this.addOptionHandler();
        });
    }

    addOptionHandler() {
        this.optionsInlineCount = this.optionsInlineCount + 1;

            document.querySelector('.field-options .options-input-block'
                ).insertAdjacentHTML('beforeend', this.makeAddOptionEle());

            this.optionInputDelete();
            this.optionNameHandler();
            this.optionValueHandler();
    }

    addAllOption() {
        document.getElementById('add-all-option-btn').addEventListener('click', e => {
            this.setOptionsObject();
        });
    }

    setOptionsObject() {
        const optionsBlock = document.querySelector('.options-input-block');
        const options = optionsBlock.querySelectorAll('.inline-related');
        const optionResult = optionsBlock.querySelectorAll('.option-result');
        const keys = Object.keys(this.optionObject);
    
        if (optionResult.length == 0) {
            alert('추가된 옵션이 없습니다. 옵션을 먼저 추가해주세요.');
            return false;
        };
        
        options.forEach(ele => {
            const key = ele.querySelector('.class_option_name').value;
            const values = ele.querySelectorAll('.option-result .option-badge-text');

            this.optionObject[key] = new Array();

            values.forEach(value => {
                this.optionObject[key].push(value.innerText);
            });
        });

        this.addAllOptionHandler();
    }

    setOptionInput() {
        const options = document.getElementById('id_options').value;

        if (options !== '') {
            Object.assign(this.optionObject, JSON.parse(options));

            const keys = Object.keys(this.optionObject);

            keys.forEach(key => {
                this.addOptionHandler();

                document.getElementById(
                    `id_option_name_${this.optionsInlineCount}`).value = key;

                this.optionObject[key].forEach(value => {
                    this.optionBadgeHandler(this.optionsInlineCount, value);
                });
            });
        }
    }

    addAllOptionHandler() {
        const items = document.querySelectorAll('.dynamic-itemreal_item');
        const itemsValue = (Array.from(items)).map( e => { return e.querySelector('.field-name input').value; });
        const itemsLen = items.length;
        let i = 0;

        document.getElementById('id_options').value = JSON.stringify(this.optionObject);

        this.arrayProduct(Object.values(this.optionObject)).forEach((ele) => {
            if (itemsValue.indexOf(ele.join('/')) === -1) {
                document.querySelector('#itemreal_item-group .add-row a').click();
                document.getElementById(`id_itemreal_item-${i+itemsLen}-name`).value = ele.join('/');
                i++;
            }
        });
    }

    optionInputDelete() {
        document.getElementById(
            `option_input_delete_${this.optionsInlineCount}`).addEventListener('click', e => {
                e.preventDefault();
                const id = e.target.getAttribute('data-id');
               
                document.getElementById(`inline_related_${id}`).remove();
                this.optionsInlineCount = this.optionsInlineCount - 1;

                this.optionRename(id);
            }
        );
    }

    optionBadgeDelete(e) {
        e.preventDefault();
        e.currentTarget.parentNode.remove();
    }
}

const option = new Option();
option.setOptionInput();
option.addOption();
option.addAllOption();