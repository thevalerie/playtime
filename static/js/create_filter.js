"use strict";


function sendFilterData(evt) {
    evt.preventDefault();

    let payload = {
        'data': $(this).serialize()
        };

    console.log(payload)

    $.post('/create_filter', payload, function(data) {
        console.log(data);
        });    
}

$("#newFilterForm").on('submit', sendFilterData);
