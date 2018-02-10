"use strict";

function displayRetailer(results){
    var retailer_dict = results;
    $('#retailer').html(retailer_dict["retailer"]);

}

$('#brand').on('click', ".chosen-brand", function() {
    var brand = $(this).html();
    $.post("/affinity.json", {"brand": brand}, displayRetailer);
});
