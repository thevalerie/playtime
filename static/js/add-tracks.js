"use strict";

let tracksToAdd = new Set();

$(document).ready(function() {

    if ($('#playlistTable').length) {
        $('#selectPlaylist').hide();
    }
    
})


// handle displaying the add checkboxes & drop-down

function displayAddCheckboxes() {
    
    tracksToAdd.clear();
    $('#select-all-add').prop('checked', false)
    $('.selected-track-add').prop('checked', false)
    $('.select-add').toggle();
    $('#selectPlaylist').toggle();
    $('#saveChanges').toggle();
}

$('#activateAdd').on('click', displayAddCheckboxes)

// handle checking/unchecking the "check all" checkbox

function selectDeselectAdd(evt) {
    
    if ($(this).prop('checked')) {
        $('.selected-track-add').prop('checked', true)
    } else {
        $('.selected-track-add').prop('checked', false)
    }
}

$('#select-all-add').on('click', selectDeselectAdd)

// handle checking/unchecking a single checkbox

function selectTrackToAdd(evt) {

    let trackId = $(this).prop('value')

    // if the box is being checked, add it to the set of tracks to add
    if ($(this).prop('checked')) {
        tracksToAdd.add(trackId);
        console.log(tracksToAdd)
    } else {
    // if the select all box is already checked, un-check it
        if ($('#select-all-add').prop('checked')) {
            $('#select-all-add').prop('checked', false)
        }
    // also remove the track ID from the set of tracks to add
        tracksToAdd.delete($(this).val())
    }
}

$('.selected-track-add').on('click', selectTrackToAdd)

// handle drop-down confirming adding tracks to playlist

function addTracksPlaylist(evt) {

    if (! tracksToAdd) {
        console.log('No tracks selected!')
    
    } else {

        let TrackIds = Array.from(tracksToAdd)

        // send a post request to add the tracks
        let payload = {'playlist_id': $(this).data('playlistId'),
                       'track_ids[]': TrackIds};

        $.post('/add_tracks_playlist.json', payload, function(data) {

            console.log(data);
            tracksToAdd.clear();
            $('#select-all-add').prop('checked', false)
            $('.selected-track-add').prop('checked', false)

            if ($('#playlistTable').length) {

                $('.select-add').hide();
                $('#selectPlaylist').hide();
                $('#saveChanges').show();
            }
        });

    }
}

$('.addToPlaylist').on('click', addTracksPlaylist)

// handle adding from one playlist to another

// def function addFromPlaylist(evt) {

//         let payload = {'source_playlist_id': $('#tracksTable').data('playlistId'),
//                        'target_playlist_id': $(this).data('playlistId'),
//                        'track_ids[]': TrackIds};

//         $.post('/add_tracks_playlist', payload, function(data) {
//             console.log(data);
//             tracksToAdd.clear();
//             $('#select-all-add').prop('checked', false)
//             $('.selected-track-add').prop('checked', false)
//             $('.select-add').hide();
//             $('#selectPlaylist').hide();
//             $('#saveChanges').show();
//             });
// }

// // handle adding from recommendations

// def function addFromRecommendations(evt) {

//         let payload = {'target_playlist_id': $(this).data('playlistId'),
//                        'track_ids[]': TrackIds};

//         $.post('/add_recommended_tracks', payload, function(data) {
//             console.log(data);
//             tracksToAdd.clear();
//             $('#select-all-add').prop('checked', false)
//             $('.selected-track-add').prop('checked', false)
//             });
// }

