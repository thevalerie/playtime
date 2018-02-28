"use strict";

function tagTracksInCategory(data) {
    
    console.log('tracks received:', data);

    let trackIds = data.matchingTracks;

    // change the HTML text of the track-category td child elements to the category name
    $('.track').each(function() { 
        console.log($(this).data('trackId'));
        console.log(trackIds);
        console.log(trackIds.includes($(this).data('trackId')));
        if (trackIds.includes($(this).data('trackId'))) {
            $(this).children('td.track-category').text(data.categoryName);
        }
    });
    // make all the track-category elements visible
    $('.track-category').show();
}


function showCategories(evt) {

    let payload = {
        'cat_id': $(this).children('option:selected').data('catId'),
        'playlist_id': $('#tracksTable').data('playlistId')
    };
    console.log(payload)

    $.get('/check_category.json', payload, (data => tagTracksInCategory(data))
    );
}


$('#selected-category').on('change', showCategories)
