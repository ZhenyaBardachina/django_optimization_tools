'use strict';

let orderItemNum, deltaQuantity, orderItemQuantity, deltaCost;
let productPrices = [];
let quantityArr = [];
let priceArr = [];

let totalForms;
let orderTotalQuantity;
let orderTotalCost;

let $orderTotalQuantityDOM;
let $orderTotalCost;
let $orderForm;



function parseOrderForm() {
    for (let i = 0; i < totalForms; i++) {
        let quantity = parseInt($('input[name="items-' + i + '-quantity"]').val());
        let price = parseFloat($('.items-' + i + '-price').text().replace(',', '.'));
        quantityArr[i] = quantity;
        priceArr[i] = (price) ? price : 0;
    }
}

function renderSummary(orderTotalQuantity, orderTotalCost) {
    $orderTotalQuantityDOM.html(orderTotalQuantity.toString());
    $orderTotalCost.html(Number(orderTotalCost.toFixed(2)).toString().replace('.', ','));
}

function updateTotalQuantity() {
    orderTotalQuantity = 0;
    orderTotalCost = 0;
    for (let i = 0; i < totalForms; i++) {
        orderTotalQuantity += quantityArr[i];
        orderTotalCost += quantityArr[i] * priceArr[i];
    }
    renderSummary(orderTotalQuantity, orderTotalCost);
}

function orderSummaryUpdate(orderitemPrice, deltaQuantity) {
    orderTotalQuantity += deltaQuantity;
    deltaCost = orderitemPrice * deltaQuantity;
    orderTotalCost += deltaCost;
    renderSummary(orderTotalQuantity, orderTotalCost);
}


function deleteOrderItem(row) {
    let targetName = row[0].querySelector('input[type="number"]').name;
    orderItemNum = parseInt(targetName.replace('items-', '').replace('-quantity', ''));
    deltaQuantity = -quantityArr[orderItemNum];
    orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity);
}


window.onload = function () {
    console.log('order DOM ready');

    totalForms = parseInt(document.querySelector('input[name="items-TOTAL_FORMS"]').value);

    $orderTotalQuantityDOM = $('.order_total_quantity');
    orderTotalQuantity = parseInt($orderTotalQuantityDOM.text()) || 0;

    $orderTotalCost = $('.order_total_cost');
    orderTotalCost = parseFloat($orderTotalCost.text().replace(',', '.')) || 0;

    parseOrderForm();

    if (!orderTotalQuantity) {
        updateTotalQuantity();
    }

    $orderForm = $('.order_form');
    $orderForm.on('change', 'input[type="number"]', function (event) {
    console.log('change', orderItemNum)
        orderItemNum = parseInt(event.target.name.replace('items-', '').replace('-quantity', ''));
        if (priceArr[orderItemNum]) {
            orderItemQuantity = parseInt(event.target.value);
            deltaQuantity = orderItemQuantity - quantityArr[orderItemNum];
            quantityArr[orderItemNum] = orderItemQuantity;
            orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity);
        }
    });

        $orderForm.on('change', 'input[type="checkbox"]', function (event) {
        orderItemNum = parseInt(event.target.name.replace('items-', '').replace('-DELETE', ''));
        if (event.target.checked) {
            deltaQuantity = -quantityArr[orderItemNum];
        } else {
            deltaQuantity = quantityArr[orderItemNum];
        }
        orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity);
    });

    $('.formset_row').formset( {
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'items',
        removed: deleteOrderItem,
    });
}

//    let formset = $('#richtextcontent_set-group .inline-related').formset;
//      на форуме пишут, что должно помочь, но я либо не туда пишу, либо всё таки не работает в этом случае


