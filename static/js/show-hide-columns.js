"use strict";

// start with default column view
$('.default-hide').hide();


// show modal for customize column view

$('#showHideColumnsBtn').on('click', function() {
    $('#showHideColumnsModal').show();
});


// toggle columns show/hide

function showHideColumns(evt) {

    let to_toggle = $(this).prop('value');
    console.log(to_toggle)
    $('.' + to_toggle).toggle()

}

$(".column-checkbox").on('click', showHideColumns);


// reset to default column view

function resetColumnView(evt) {

    // reset the column view to the default
    $('.default-show').show();
    $('.default-hide').hide();

    // reset checkboxes to the default
    $('.default-checked').prop('checked', true);
    $('.default-unchecked').prop('checked', false);
}

$('#reset-columns').on('click', resetColumnView);