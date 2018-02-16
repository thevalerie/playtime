"use strict";


function sendChanges(evt) {
    
    let payload = {
        'playlist_id': $(this).attr('data-playlist-id')
    };

    $.post('/push_to_spotify', payload, function(data) {
        console.log(data);
        });    
}

$("#saveChanges").on('click', sendChanges);
