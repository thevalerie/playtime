"use strict";

$('#saveDelete').hide();
let tracksToDelete = new Set();

// handle displaying the delete checkboxes & button

function displayDeleteCheckboxes() {
    
    tracksToDelete.clear();
    $('#select-all-delete').prop('checked', false)
    $('.selected-track-delete').prop('checked', false)
    $('.select-delete').toggle();
    $('#saveDelete').toggle();
    $('#saveChanges').toggle();
}

$('#activateDelete').on('click', displayDeleteCheckboxes)

// handle checking/unchecking the "check all" checkbox

function selectDeselectDelete(evt) {
    
    if ($(this).prop('checked')) {
        $('.selected-track-delete').prop('checked', true)
    } else {
        $('.selected-track-delete').prop('checked', false)
    }
}

$('#select-all-delete').on('click', selectDeselectDelete)

// handle checking/unchecking a single checkbox

function selectTrackToDelete(evt) {

    let trackId = $(this).prop('value')

    // if the box is being checked, add it to the set of tracks to delete
    if ($(this).prop('checked')) {
        tracksToDelete.add(trackId)
        console.log(tracksToDelete)
    } else {
    // if the select all box is already checked, un-check it
        if ($('#select-all-delete').prop('checked')) {
            $('#select-all-delete').prop('checked', false)
        }
    // also remove the track ID from the set of tracks to delete
        tracksToDelete.delete($(this).val())
    }
}

$('.selected-track-delete').on('click', selectTrackToDelete)

// handle button confirming delete tracks from playlist

function deleteTracksPlaylist(evt) {
    if (! tracksToDelete) {
        console.log('No tracks selected!')
    } else {

        let trackIds = Array.from(tracksToDelete)
        // send a post request to delete the tracks
        let payload = {'playlist_id': $(this).data('playlistId'),
                       'track_ids[]': trackIds};

        $.post('/delete_tracks_playlist', payload, function(playlist_id) {
            window.location.replace('/playlist/' + playlist_id);
            });

        tracksToDelete.clear();
        $('#select-all-delete').prop('checked', false)
        $('.selected-track-delete').prop('checked', false)
        $('.select-delete').hide();
        $('#saveDelete').hide();
        $('#saveChanges').show();
    }
}

$('#saveDelete').on('click', deleteTracksPlaylist)
