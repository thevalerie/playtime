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
    $('.track').each(function(i) {
        $(this).attr('data-position', i);
    });
}

function updateTrackOrderDB() {
    // $.ajax('/reorder', {}, reorderTracks);
    // console.log("Finished sending AJAX")

}


$("#tracksTable").sortable( {
    helper: reorderTracks,
    stop: updateTrackOrder
    }).disableSelection();
