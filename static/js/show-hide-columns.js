"use strict";

$('.track-album').hide();
$('.track-danceability').hide();
$('.track-energy').hide();
$('.track-valence').hide();
$('.track-is-explicit').hide();
$('.track-category').hide();

// show modal for customize column view

$('#showHideColumnsBtn').on('click', function() {
    $('#showHideColumnsModal').show();
});

$(window).on('click', function(evt) {
    if (evt.target == $('#showHideColumnsModal')) {
        $('#showHideColumnsModal').hide();
    }
});

// toggle columns show/hide

function showHideColumns(evt) {

    let to_toggle = $(this).prop('value');
    console.log(to_toggle)
    $('.' + to_toggle).toggle()

}

$(".column-checkbox").on('click', showHideColumns);
