"use strict";

// helper functions

function toPercentage(decimal) {

    return Math.round(decimal * 100).toString() + '%'
}

function toMinsSecs(millisecs) {

    let mins = milliseconds / 60000
    let secs = (milliseconds % 60000) / 1000

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
        if (catInfo.exclude_explicit) {
            $('#exclude_explicit').text('Yes')
        }
        if (catInfo.duration_min) {
            $('#duration_min').text(toMinsSecs(catInfo.duration_min))
        }
        if (catInfo.duration_max) {
            $('#duration_max').text(toMinsSecs(catInfo.duration_max))
        }
        if (catInfo.tempo_min) {
            $('#tempo_min').text(catInfo.tempo_min)
        }
        if (catInfo.tempo_max) {
            $('#tempo_max').text(catInfo.tempo_max)
        }
        if (catInfo.danceability_min) {
            $('#danceability_min').text(toPercentage(catInfo.danceability_min))
        }
        if (catInfo.danceability_max) {
            $('#danceability_max').text(toPercentage(catInfo.danceability_max))
        }
        if (catInfo.energy_min) {
            $('#energy_min').text(toPercentage(catInfo.energy_min))
        }
        if (catInfo.energy_max) {
            $('#energy_max').text(toPercentage(catInfo.energy_max))
        }
        if (catInfo.valence_min) {
            $('#valence_min').text(toPercentage(catInfo.valence_min))
        }
        if (catInfo.valence_max) {
            $('#valence_max').text(toPercentage(catInfo.valence_max))
        }

    $('#viewCatModal').show();
});

$(window).on('click', function(evt) {
    if (evt.target == $('#viewCatModal')) {
        $('#viewCatModal').hide();
    }
});

// show modal for new category form

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
        });    
}

$("#newCategoryForm").on('submit', sendCategoryData);
