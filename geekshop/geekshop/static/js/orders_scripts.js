'use sctrict';


window.onload = function () {
    console.log("order DOM ready");

    let _quantity, _price, orderitem_num, delta_quantity, delta_cost;

    let quantity_arr = [];
    let price_arr = [];

    let total_forms = parseInt($('input[name="items-TOTAL_FORMS"]').val());

    let order_total_quantity = parseFloat($('.order_total_quantity').text().replace(',', '.'));
    let order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.'));


    for (let i=0; i < total_forms; i++) {
       _quantity = parseInt($('input[name="items-' + i + '-quantity"]').val());
       _price = parseFloat($('.items-' + i + '-price').text().replace(',', '.'));
       quantity_arr[i] = _quantity;
       if (_price) {
           price_arr[i] = _price;
       } else {
           price_arr[i] = 0;
       }
    }

    $('.order_form').on('change', 'input[type="number"]', function () {
       var target = event.target;
       orderitem_num = parseInt(target.name.replace('items-', '').replace('-quantity', ''));
       if (price_arr[orderitem_num]) {
           orderitem_quantity = parseInt(target.value);
           delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
           quantity_arr[orderitem_num] = orderitem_quantity;

           orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
       }
    });

    $('.order_form').on('change', 'input[type="checkbox"]', function (event) {
        orderitem_num = parseInt(event.target.name.replace('items-', '').replace('-DELETE', ''));
        if (event.target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
        } else {
            delta_quantity = quantity_arr[orderitem_num];
        }
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    });


    function orderSummaryUpdate(orderitem_price, delta_quantity) {
       delta_cost = orderitem_price * delta_quantity;

       order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
       order_total_quantity = order_total_quantity + delta_quantity;

       $('.order_total_cost').html(order_total_cost.toString());
       $('.order_total_quantity').html(order_total_quantity.toString());
    }


    if (!order_total_quantity) {
   orderSummaryRecalc();
}

    function orderSummaryRecalc() {
       order_total_quantity = 0;
       order_total_cost = 0;

       for (let i=0; i < total_forms; i++) {
           order_total_quantity += quantity_arr[i];
           order_total_cost += price_arr[i];
       }
       $('.order_total_quantity').html(order_total_quantity.toString());
       $('.order_total_cost').html(order_total_cost.toFixed(2).toString());
    }


    function deleteOrderItem(row) {
       let target_name= row[0].querySelector('input[type="number"]').name;
       orderitem_num = parseInt(target_name.replace('items-', '').replace('-quantity', ''));
       delta_quantity = -quantity_arr[orderitem_num];
       orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    }

    $('.order_form select').change(function () {
       let target = event.target;
       orderitem_num = parseInt(target.name.replace('items-', '').replace('-product', ''));
       let orderitem_product_pk = target.options[target.selectedIndex].value;


   if (orderitem_product_pk) {
       $.ajax({
           url: "/orders/product/" + orderitem_product_pk + "/price/",
           success: function (data) {
               if (data.price) {
                   price_arr[orderitem_num] = parseFloat(data.price);
                   if (isNaN(quantity_arr[orderitem_num])) {
                       quantity_arr[orderitem_num] = 0;
                   }
                   let price_html = '<span class="items-' + orderitem_num + 'price">' + data.price.toString().replace('.', ',') + '</span> руб';
                   let current_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');


                   current_tr.find('td:eq(2)').html(price_html);

                   if (isNaN(current_tr.find('input[type="number"]').val())) {
                       current_tr.find('input[type="number"]').val(0);
                   }
                   orderSummaryRecalc();
                   }
               },
           });
       }
   });


    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'items',
        removed: deleteOrderItem
    });

}  // end block window.onload