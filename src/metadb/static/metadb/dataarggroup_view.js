$(document).ready( function () {
     // Create arguments group table
     var apiURL = $('#tab-dataarggroup').attr('api-data-url')

     dataarggroup_columns = [
         {'render': function() { return null; }},  // For checkboxes
         {'render': (data, type, row, meta) => {
             return renderButtons(row, apiURL)
         }},  // for buttons
         {'data': 'id'},
         {'data': 'name'},
         {'data': 'description'},
         {'data': function(data, type, row, meta) {
             specific_parameters = Array();
             data.specific_parameter.forEach(element => {
                 specific_parameters.push(element.string);
             });
             if (data.specific_parameter.length == 0) {
                 specific_parameters.push('-');
             }
             return specific_parameters.join('; <br>');
         }},
     ]
     
     dataarggroup_columnsDefs = [
         { width: '20px', targets: 0, orderable: false, className: 'select-checkbox' }, // Select checkbox
         { width: '45px', targets: 1, orderable: false, }, // Buttons
         { width: '65px', targets: 2, },   // id
         { width: '105px', targets: 3 },    // name
         { width: '275px', targets: 4 },   // description
         { width: '375px', targets: 5 },   // specific parameters
     ]

    var dataarggroupOptions = $.extend(true, {}, commonOptions);
    dataarggroupOptions["columnDefs"] = dataarggroup_columnsDefs.concat(all_columns_defs);
    dataarggroupOptions["columns"] = dataarggroup_columns;
    dataarggroupOptions["ajax"] = { 'url': apiURL, 'type': 'GET', 'dataSrc': 'data' };
    $('#main-tabs a[href="#tab-dataarggroup"]').on('click', function() {
        if (!$.fn.DataTable.isDataTable('#dataarggroup')) {
            $('#dataarggroup').DataTable( dataarggroupOptions ).on('draw', function() {
                addUpdDelButtonHandlers.call(this, 'dataarggroup');
            });
            $('#dataarggroup').DataTable().on('xhr.dt', set_header);
        }
    });
});