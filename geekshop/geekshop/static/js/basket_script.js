'use strict';

window.onload = function () {
    console.log('DOM is ready');
    $('.basket_record').on('change', 'input[type="number"]', function(event) {
        let quantity = event.target.value;
        let basketPk = event.target.name;
//        console.log(basketPk, quantity);
        $.ajax({
            url: "/basket/update/" + basketPk + "/" + quantity + "/",
            success: function(data) {
                if (data.status) {
                    $('.basket_summary').html(data.basket_summary);
                }
            },
        });
    });
}