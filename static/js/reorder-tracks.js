"use strict";

function reorderTracks(e, tr) {
    let originals = tr.children();
    let helper = tr.clone();
    // helper.children().each(function(track) {
    //     $(this).width(originals.eq(track).width())
    // });
    return helper;
}

// function updateTrackOrder() {
//     $.post('/reorder', {}, reorderTracks);
//     console.log("Finished sending AJAX")
// }

$("#tracksTable").sortable( {
    helper: reorderTracks,    
    }).disableSelection();




// var fixHelperModified = function(e, tr) {
//     var $originals = tr.children();
//     var $helper = tr.clone();
//     $helper.children().each(function(index) {
//         $(this).width($originals.eq(index).width())
//     });
//     return $helper;
// },
//     updateIndex = function(e, ui) {
//         $('td.index', ui.item.parent()).each(function (i) {
//             $(this).html(i + 1);
//         });
//     };

// $("#tracksTable").sortable( {
//     helper: fixHelperModified,
//     stop: updateIndex
// }).disableSelection();