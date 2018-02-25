"use strict";

function tagTracksInCategory(data) {
    console.log('tracks received:', data);
    // select all the track elements where the playlist-id is in the list
    let trackIds = data.matchingTracks;
    // whyyyy is this not filtering?
    let tracksInCategory = $('.track').filter(track => 
        trackIds.includes($(this).data('trackId')));
    console.log(tracksInCategory);
    // change the inner HTML of the track-category td child elements to the category name
    tracksInCategory.each(trackRowElement => 
        $(this).children('td.track-category').innerHTML = data.categoryName);
    // make all the track-category elements visible
    $('.track-category').show();
}


function showCategories(evt) {

    let payload = {
        'cat_id': $(this).children('option:selected').data('catId'),
        'playlist_id': $('#tracksTable').data('playlistId')
    };

    $.get('/check_category.json', payload, (data => tagTracksInCategory(data))
    );
}


$('#selected-category').on('change', showCategories)
