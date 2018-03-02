"use strict";

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

// show modal to view category info

$('.catListing').on('click', function(evt) {

    let catInfo = $(this).data('json');
    $('#catRecommend').val(catInfo.cat_id)

    // replace HTML values in the modal with data for the category selected
    $('#category-name').text(catInfo.cat_name)
    $('#exclude_explicit').text(displayIfValid(catInfo.exclude_explicit))
    $('#min_duration_ms').text(toMinsSecs(catInfo.min_duration_ms))
    $('#max_duration_ms').text(toMinsSecs(catInfo.max_duration_ms))
    $('#min_tempo').text(displayIfValid(catInfo.min_tempo))
    $('#max_tempo').text(displayIfValid(catInfo.max_tempo))
    $('#min_danceability').text(toPercentage(catInfo.min_danceability))
    $('#max_danceability').text(toPercentage(catInfo.max_danceability))
    $('#min_energy').text(toPercentage(catInfo.min_energy))
    $('#max_energy').text(toPercentage(catInfo.max_energy))
    $('#min_valence').text(toPercentage(catInfo.min_valence))
    $('#max_valence').text(toPercentage(catInfo.max_valence))

    $('#viewCatModal').show();
});


// show modal for new category form

$('#newCatBtn').on('click', function() {
    $('#newCatModal').show();
});


// reset new category form when the modal is closed

$('.clr-form').on('click', function() {
    $('#newCategoryForm').trigger("reset");
});

$(window).on('click', function(evt) {
    if (evt.target != $('#newCatModal')) {
        $('#newCategoryForm').trigger("reset");
    }
});

// submit form to create a new category

function sendCategoryData(evt) {
    evt.preventDefault();

    console.log($(this));

    $.post('/create_category.json', $(this).serialize(), function(data) {
        $('#newCatModal').hide();
        window.location.replace('/my_categories');
        });
}

$("#newCategoryForm").on('submit', sendCategoryData);
