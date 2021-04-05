$(document).ready( function () {
     // Create arguments group table
     var apiURL = $('#tab-procarggroup').attr('api-data-url')

     var procarggroup_columns = [
         { 'render': function() { return null; } },  // For checkboxes
         {'render': (data, type, row, meta) => {
             return renderButtons(row, apiURL)
         }},  // for buttons
         { 'data': 'arguments_group.id' },
         { 'data': 'arguments_group.name' },
         { 'data': 'arguments_group.description' },
         { 'data': 'processor.processori18n.name' },
         { 'data': 'combination.string' }
     ];
     
     var procarggroup_columnsDefs = [
         { width: '20px', targets: 0, orderable: false, className: 'select-checkbox' }, // Select checkbox
         { width: '45px', targets: 1, orderable: false, }, // Buttons
         { width: '65px', targets: 2, },   // id
         { width: '105px', targets: 3 },    // name
         { width: '175px', targets: 4 },   // description
         { width: '275px', targets: 5 },   // processor
         { width: '200px', targets: 6 }   // combination
     ];

    var procarggroupOptions = $.extend(true, {}, commonOptions);
    procarggroupOptions["columnDefs"] = procarggroup_columnsDefs.concat(all_columns_defs);
    procarggroupOptions["columns"] = procarggroup_columns;
    procarggroupOptions["ajax"] = { 'url': apiURL, 'type': 'GET', 'dataSrc': 'data' };
    $('#main-tabs a[href="#tab-procarggroup"]').on('click', function() {
        if (!$.fn.DataTable.isDataTable('#procarggroup')) {
            $('#procarggroup').DataTable( procarggroupOptions ).on('draw', function() {
                addUpdDelButtonHandlers.call(this, 'procarggroup');
            });
            $('#procarggroup').DataTable().on('xhr.dt', set_header);
        }
    });
});