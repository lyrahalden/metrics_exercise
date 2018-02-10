"use strict";

function displayRetailer(results){
    var retailer_dict = results;
    console.log(retailer_dict["retailer"]);
    $('#retailer').html(retailer_dict["retailer"]);

}

$('#brand').on('click', ".chosen-brand", function() {
    var brand = $(this).html();
    console.log(brand);
    $.post("/affinity.json", {"brand": brand}, displayRetailer);
});
