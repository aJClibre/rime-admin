/*
 * Author: Abdullah A Almsaeed
 * Date: 4 Jan 2014
 * Description:
 *      This is a demo file used only for the main dashboard (index.html)
 **/

$(function() {
    "use strict";

   //console.log('start'); 
    $.ajax({
        url: "ajax/ajax.py",
        type: "post",
        dataType: "json",
        data: {
            'small-boxes': {
                'fields_where' : 'NB de cas',
                'fields_select' : "form_response, incident_title, incident_description, DATE_FORMAT(incident_date, '%d/%m/%Y %H:%i'), location_name, latitude, longitude"
            }/*,
            'big-boxes': {
                'fields_where' : 'toto',
                'fields_select': 'tata'
            }*/
        },
        success: function(response) {

            // test if no error in the server treament 
            if (response.message === "") {
                console.log('ajax/testPsyco.py no response.message ');
                
                //
                // small boxes
                //
                var sb = response['small-boxes'],
                sb_data = sb.data,
                total = 0,
                i;
                
                // rapport
                $("#sb-rapport>h3").html(sb_data.length);

                // total
                for (i=0; i<sb_data.length; i++) {
                    total += sb_data[i][0];
                }

                $("#sb-total>h3").html(total);
                $("#sb-total>p").html(sb.params['fields_where']);

                //
                // mapbox
                //
                $("#mapbox>div>h3").html(sb.params['fields_where']);
            }

            else alert('ERROR : '+ response.message);

        },
        error: function(err) {
            console.dir(err);
        }
    });
    
    
    //Make the dashboard widgets sortable Using jquery UI
    $(".connectedSortable").sortable({
        placeholder: "sort-highlight",
        connectWith: ".connectedSortable",
        handle: ".box-header, .nav-tabs",
        forcePlaceholderSize: true,
        zIndex: 999999
    }).disableSelection();
    $(".connectedSortable .box-header, .connectedSortable .nav-tabs-custom").css("cursor", "move");
    //jQuery UI sortable for the todo list
    $(".todo-list").sortable({
        placeholder: "sort-highlight",
        handle: ".handle",
        forcePlaceholderSize: true,
        zIndex: 999999
    }).disableSelection();
    

    //bootstrap WYSIHTML5 - text editor
    $(".textarea").wysihtml5();

    $('.daterange').daterangepicker(
            {
                ranges: {
                    'Today': [moment(), moment()],
                    'Yesterday': [moment().subtract('days', 1), moment().subtract('days', 1)],
                    'Last 7 Days': [moment().subtract('days', 6), moment()],
                    'Last 30 Days': [moment().subtract('days', 29), moment()],
                    'This Month': [moment().startOf('month'), moment().endOf('month')],
                    'Last Month': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')]
                },
                startDate: moment().subtract('days', 29),
                endDate: moment()
            },
    function(start, end) {
        alert("You chose: " + start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    });

    /* jQueryKnob */
    $(".knob").knob();

    //jvectormap data
    var visitorsData = {
        "US": 398, //USA
        "SA": 400, //Saudi Arabia
        "CA": 1000, //Canada
        "DE": 500, //Germany
        "FR": 760, //France
        "CN": 300, //China
        "AU": 700, //Australia
        "BR": 600, //Brazil
        "IN": 800, //India
        "GB": 320, //Great Britain
        "RU": 3000 //Russia
    };
    //World map by jvectormap
    $('#world-map').vectorMap({
        map: 'world_mill_en',
        backgroundColor: "transparent",
        regionStyle: {
            initial: {
                fill: '#e4e4e4',
                "fill-opacity": 1,
                stroke: 'none',
                "stroke-width": 0,
                "stroke-opacity": 1
            }
        },
        series: {
            regions: [{
                    values: visitorsData,
                    scale: ["#92c1dc", "#ebf4f9"],
                    normalizeFunction: 'polynomial'
                }]
        },
        onRegionLabelShow: function(e, el, code) {
            if (typeof visitorsData[code] != "undefined")
                el.html(el.html() + ': ' + visitorsData[code]);
        }
    });


});
