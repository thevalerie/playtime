"use strict";

function reorderTracks(evt, tr) {
    let originals = tr.children();
    let helper = tr.clone();
    helper.children().each(function(track) {
        $(this).width(originals.eq(track).width())
    });
    return helper;
}

function updateTrackOrder(evt) {

    let newTrackOrder = new Object()

    $('.track').each(function(i) {
        $(this).attr('data-position', i);
        newTrackOrder[$(this).attr('data-pt-id')] = $(this).attr('data-position')
    });

    $.post('/reorder', {'new_track_order' : JSON.stringify(newTrackOrder)},
                        function(data){ console.log(data) });

}


$("#tracksTable").sortable( {
    helper: reorderTracks,
    stop: updateTrackOrder
    }).disableSelection();
