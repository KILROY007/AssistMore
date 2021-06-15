$(function () {
    //Json data by api call for order table
    $.get(orderListApiUrl, function (response) {
        if(response) {
            var table = '';
            var totalCost = 0;
            $.each(response, function(index, order) {
                totalCost += parseFloat(order.total);
                table += '<tr>' +
                    '<td>'+ order.datetime +'</td>'+
                    '<td>'+ order.order_id +'</td>'+
                    '<td>'+ order.customer_name +'</td>'+
                    '<td>'+ order.total.toFixed(2) +' Rs</td>'+
                    '<td><span class="btn btn-xs btn-danger delete-order">Delete</span></td></tr>';
            });
            table += '<tr><td colspan="3" style="text-align: end"><b>Total</b></td><td><b>'+ totalCost.toFixed(2) +' Rs</b></td></tr>';
            $("table").find('tbody').empty().html(table);
        }
    });
});

$(document).on("click", ".delete-order", function (){
    var tr = $(this).closest('tr');
    var data = {
        order_id : tr.data('id')
    };
    var isDelete = confirm("Are you sure to delete this  item?");
    if (isDelete) {
        callApi("POST", orderDeleteApiUrl, data);
    }
});