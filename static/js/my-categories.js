"use strict";

// show modal for new category form

$('#newCatBtn').on('click', function() {
    $('#newCatModal').show();
});

// reset new category form when the modal is closed

$('.clr-form').on('click', function() {
    $('#newCategoryForm').trigger("reset");
});

// $(window).on('click', function(evt) {
//     $('#newCategoryForm').trigger("reset");
// }).on('click', $('#newCatModal'), function(evt) {
//     evt.stopPropagation();
// });

// submit form to create a new category

function sendCategoryData(evt) {
    evt.preventDefault();

    $.post('/create_category.json', $(this).serialize(), function(data) {
        $('#newCatModal').hide();
        window.location.replace('/my_categories');
        });
}

$("#newCategoryForm").on('submit', sendCategoryData);

// show modal to view category info

$('.catListing').on('click', function(evt) {

    let catInfo = $(this).data('json');

    // replace HTML values in the modal with data for the category selected
    $('#cat-id-recommend').data('catId', catInfo.cat_id);
    $('#cat-id-recommend').attr('href', '/get_recommendations/' + catInfo.cat_id)

    $('#category-name').text(catInfo.cat_name);
    $('#min_duration_ms').text(toMinsSecs(catInfo.min_duration_ms));
    $('#max_duration_ms').text(toMinsSecs(catInfo.max_duration_ms));
    $('#min_tempo').text(displayIfValid(catInfo.min_tempo));
    $('#max_tempo').text(displayIfValid(catInfo.max_tempo));
    $('#min_danceability').text(toPercentage(catInfo.min_danceability));
    $('#max_danceability').text(toPercentage(catInfo.max_danceability));
    $('#min_energy').text(toPercentage(catInfo.min_energy));
    $('#max_energy').text(toPercentage(catInfo.max_energy));
    $('#min_valence').text(toPercentage(catInfo.min_valence));
    $('#max_valence').text(toPercentage(catInfo.max_valence));

    if (catInfo.exclude_explicit) {
        $('#exclude_explicit').text('Yes'); 
    } else {
        $('#exclude_explicit').text('No'); 
    }

    $('#viewCatModal').show();
});

// close modal when button to get recommendations is clicked

// $('#cat-id-recommend').on('click', function(){
//     $('#viewCatModal').hide();
//         window.location.replace('/my_categories');
// })

// helper functions

function toPercentage(decimal) {
    if (decimal) {
        return Math.round(decimal * 100).toString() + '%'
    } else {
        return 'None'
    }
}

function toMinsSecs(millisecs) {

    if (millisecs) {
        let mins = Math.floor(millisecs / 60000)
        let secs = (millisecs % 60000) / 1000

        if (secs < 10) {
            return mins.toString() + ':0' + secs.toString()
        } else {
            return mins.toString() + ':' + secs.toString()
        }
    } else {
        return 'None'
    }
}

function displayIfValid(attribute) {

    if (attribute) {
        return attribute
    } else {
        return 'None'
    }
}
