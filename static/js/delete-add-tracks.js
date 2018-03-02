"use strict";


function selectDeselectDelete(evt) {
    
    if ($(this).prop('checked')) {
        $('.selected-track-delete').prop('checked', true)
    } else {
        $('.selected-track-delete').prop('checked', false)
    }
}

$('#select-all-delete').on('click', selectDeselectDelete)



function selectTrackToDelete(evt) {

    if (! $(this).prop('checked')) {
        if ($('#select-all-delete').prop('checked')) {
            $('#select-all-delete').prop('checked', false)
        }
    }
}


$('.selected-track-delete').on('click', selectTrackToDelete)