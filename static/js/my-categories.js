"use strict";

// helper functions

function toPercentage(decimal) {

    return Math.round(decimal * 100).toString() + '%'
}

function toMinsSecs(millisecs) {

    let mins = millisecs / 60000
    let secs = (millisecs % 60000) / 1000

    if (secs < 10) {
        return mins.toString() + ':0' + secs.toString()
    } else {
        return mins.toString() + ':' + secs.toString()
    }
}

// show modal to view category info

$('.catListing').on('click', function(evt) {

    let catInfo = $(this).data('json');
    console.log(catInfo)
    // replace HTML values in the modal with data for the category selected
    $('#category-name').text(catInfo.cat_name)
        $('#catRecommend').val(catInfo.cat_id)
        console.log($('#catRecommend').val())
        if (catInfo.exclude_explicit) {
            $('#exclude_explicit').text('Yes')
        }
        if (catInfo.min_duration_ms) {
            $('#min_duration_ms').text(toMinsSecs(catInfo.min_duration_ms))
        }
        if (catInfo.max_duration_ms) {
            $('#max_duration_ms').text(toMinsSecs(catInfo.max_duration_ms))
        }
        if (catInfo.min_tempo) {
            $('#min_tempo').text(catInfo.min_tempo)
        }
        if (catInfo.max_tempo) {
            $('#max_tempo').text(catInfo.max_tempo)
        }
        if (catInfo.min_danceability) {
            $('#min_danceability').text(toPercentage(catInfo.min_danceability))
        }
        if (catInfo.max_danceability) {
            $('#max_danceability').text(toPercentage(catInfo.max_danceability))
        }
        if (catInfo.min_energy) {
            $('#min_energy').text(toPercentage(catInfo.min_energy))
        }
        if (catInfo.max_energy) {
            $('#max_energy').text(toPercentage(catInfo.max_energy))
        }
        if (catInfo.min_valence) {
            $('#min_valence').text(toPercentage(catInfo.min_valence))
        }
        if (catInfo.max_valence) {
            $('#max_valence').text(toPercentage(catInfo.max_valence))
        }

    $('#viewCatModal').show();
});

$(window).on('click', function(evt) {
    if (evt.target == $('#viewCatModal')) {
        $('#viewCatModal').hide();
    }
});

// show/hide modal for new category form

$('#newCatBtn').on('click', function() {
    $('#newCatModal').show();
});

$(window).on('click', function(evt) {
    if (evt.target == $('#newCatModal')) {
        $('#newCatModal').hide();
    }
});

// submit form to create a new category

function sendCategoryData(evt) {
    evt.preventDefault();

    console.log($(this));

    $.post('/create_category.json', $(this).serialize(), function(data) {
        console.log(data);
        $('#newCatModal').hide();
        });
}

$("#newCategoryForm").on('submit', sendCategoryData);
