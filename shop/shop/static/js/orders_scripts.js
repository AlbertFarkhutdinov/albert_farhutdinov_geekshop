window.onload = function() {
    var _quantity, _price, order_item_num, delta_quantity, order_item_quantity, delta_cost;
    var quantity_arr = [];
    var price_arr = [];

    var TOTAL_FORMS = parseInt($('input[name="order_items-TOTAL_FORMS"]').val());
    var order_total_quantity = parseInt($('.order_total_quantity').text()) || 0 ;
    var order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0 ;

    for (var i=0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name="order_items-' + i + '-quantity"]').val());
        _price = parseFloat($('.order_items-' + i + '-price').text().replace(',', '.'));
        quantity_arr.push(_quantity);
        if (_price) {
            price_arr.push(_price);
        }
        else {
            price_arr.push(0);
        }
    }
    if (!order_total_quantity) {
        for (var i=0 ; i < TOTAL_FORMS; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_cost += quantity_arr[i] * price_arr[i];
        }
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
    }

    $('.order_form').on('click', 'input[type="number"]', function() {
        var target = event.target;
        order_item_num = target.name.replace('-quantity', '').slice('order_items-'.length);
        order_item_num = parseInt(order_item_num);
        if (price_arr[order_item_num]) {
            order_item_quantity = parseInt(target.value);
            delta_quantity = order_item_quantity - quantity_arr[order_item_num];
            quantity_arr[order_item_num] = order_item_quantity;
            orderSummaryUpdate(price_arr[order_item_num], delta_quantity);
        }
    });

    function deleteOrderItem(row) {
        var target_name = row[0].querySelector('input[type="number"]').name;
        order_item_num = event.target.name.replace('-quantity', '').slice('order_items-'.length);
        order_item_num = parseInt(order_item_num);
        delta_quantity = -quantity_arr[order_item_num];
        quantity_arr[order_item_num] = 0;
        if (!isNaN(price_arr[order_item_num]) && !isNaN(delta_quantity)) {
            orderSummaryUpdate(price_arr[order_item_num], delta_quantity);
        }
    }

    function orderSummaryUpdate(order_item_price, delta_quantity) {
        delta_cost = order_item_price * delta_quantity;
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;
        $('.order_total_cost').html(order_total_cost.toString());
        $('.order_total_quantity').html(order_total_quantity.toString());
    }

    $('.formset_row').formset({
        addText: 'Add product',
        deleteText: 'Delete',
        prefix: 'order_items',
        removed: deleteOrderItem
    });

    $('.order_form select').change(function() {
        var target = event.target;
        order_item_num = parseInt(target.name.replace('order_items-', '' ).replace('-product', ''));
        var order_item_product_pk = target.options[target.selectedIndex].value;
        if (order_item_product_pk) {
            $.ajax({
                url: "/order/product/" + order_item_product_pk + "/price/" ,
                success: function (data) {
                    if (data.price) {
                        price_arr[order_item_num] = parseFloat(data.price);
                        if (isNaN(quantity_arr[order_item_num])){
                            quantity_arr[order_item_num] = 0;
                        }
                        var price_html = '<span>' + data.price.toString().replace('.', ',') + '</span>&nbsp;rub.';
                        var current_tr = $('.order_form table').find('tr:eq(' + (order_item_num + 1 ) + ')');
                        current_tr.find('td:eq(2)').html(price_html);
                        if (isNaN(current_tr.find('input[type="number"]').val())) {
                            current_tr.find('input[type="number"]').val(0);
                        }
                        orderSummaryRecalculate();
                    }
                },
            });
        }
    });

    if (!order_total_quantity){
        orderSummaryRecalculate();
    }

    function orderSummaryRecalculate(){
        order_total_quantity = 0 ;
        order_total_cost = 0 ;
        for (var i = 0 ; i < TOTAL_FORMS; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_cost += quantity_arr[i] * price_arr[i];
        }
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html( Number (order_total_cost.toFixed(2)).toString());
    }
};