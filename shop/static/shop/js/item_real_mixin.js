const ItemRealMixin = {
    create_item_real_objects(ele, q=0) {
        const itemObject = new Object();
        
        _.map(ele, item => {
            const itemId = item.getAttribute('data-item-id');

            const quantity = (q === 0) ? item.querySelector('.quantity').innerText : q;
            itemObject[itemId] = quantity;
        });
        return itemObject
    }
}