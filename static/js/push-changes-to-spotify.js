"use strict";

function sendChanges(evt) {
    
    let payload = {
        'playlist_id': $(this).data('playlistId')
    };

    $.post('/push_to_spotify', payload, function(data) {
        console.log(data);
        });    
}

$("#saveChanges").on('click', sendChanges);
