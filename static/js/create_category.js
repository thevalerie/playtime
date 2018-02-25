"use strict";


function sendCategoryData(evt) {
    evt.preventDefault();

    let payload = {
        'data': $(this).serialize()
        };

    console.log(payload)

    $.post('/create_category', payload, function(data) {
        console.log(data);
        });    
}

$("#newCategoryForm").on('submit', sendCategoryData);
