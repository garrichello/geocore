var procarggroup_api_url = $('#tab-procarggroup').attr('api-data-url')

procarggroup_columns = [
    { 'render': function() { return null; } },  // For checkboxes
    { 'render': function (data, type, row, meta) {
        return '<div><button type="button" class="btn btn-warning btn-sm js-update-procarggroup"'
               + `data-url="${procarggroup_api_url}${row.id}">`
               + '<span class="glyphicon glyphicon-pencil"></span></button></div>&nbsp;'
               + '<div><button type="button" class="btn btn-danger btn-sm js-delete-procarggroup"'
               + `data-url="${procarggroup_api_url}${row.id}">`
               + '<span class="glyphicon glyphicon-trash"></span></button></div>';
    } },  // for buttons
    { 'data': 'arguments_group.id' },
    { 'data': 'arguments_group.name' },
    { 'data': 'arguments_group.description' },
    { 'data': 'processor.processori18n.name' },
    { 'data': 'combination.string' },
/*    { 'render': function(data, type, row, meta) {
        var procTable = $('<table style="border: #ddd" frame="void" rules="rows"></table>');
        row.processor.forEach(element => {
            var tr = $('<tr>');
            tr.append(`<td>${element.processor.processori18n.name}</td>`);
            var overrides = Array()
            element.override_combination.forEach(comb => {
                overrides.push(comb.string);
            })
            tr.append(`<td>${overrides.join('; ')}</td>`);
            procTable.append(tr);
        });
        return $('<div>').append(procTable).html();
    } },*/
]

procarggroup_columnsDefs = [
    { width: '20px', targets: 0, orderable: false, className: 'select-checkbox' }, // Select checkbox
    { width: '45px', targets: 1, orderable: false, }, // Buttons
    { width: '65px', targets: 2, },   // id
    { width: '105px', targets: 3 },    // name
    { width: '175px', targets: 4 },   // description
    { width: '275px', targets: 5 },   // processor
    { width: '200px', targets: 6 },   // combination
]

$(document).ready( function () {
     // Create arguments group table
    var procarggroupOptions = $.extend(true, {}, commonOptions);
    procarggroupOptions["columnDefs"] = procarggroup_columnsDefs.concat(all_columns_defs);
    procarggroupOptions["columns"] = procarggroup_columns;
    procarggroupOptions["ajax"] = { 'url': procarggroup_api_url, 'type': 'GET', 'dataSrc': 'data' };
    $('#main-tabs a[href="#tab-procarggroup"]').on('click', function() {
        if (!$.fn.DataTable.isDataTable('#procarggroup')) {
            $('#procarggroup').DataTable( procarggroupOptions ).on('draw', function() {
                addUpdDelButtonHandlers.call(this, 'procarggroup');
            });
            $('#procarggroup').DataTable().on('xhr.dt', set_header);
        }
    });
});