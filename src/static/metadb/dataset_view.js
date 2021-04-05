var dataset_api_url = $('#tab-dataset').attr('api-data-url');

var dataset_columns = [
    { 'render': function() { return null; } }, // For checkboxes
    { 'render': function (data, type, row, meta) {
        return '<div><button type="button" class="btn btn-warning btn-sm js-update-dataset"'
               + `data-url="${dataset_api_url}${row.id}/">`
               + '<span class="glyphicon glyphicon-pencil"></span></button></div>&nbsp;'
               + '<div><button type="button" class="btn btn-danger btn-sm js-delete-dataset"'
               + `data-url="${dataset_api_url}${row.id}/">`
               + '<span class="glyphicon glyphicon-trash"></span></button></div>';
    } },  // for buttons
    { 'data': 'id' },
    { 'data': 'is_visible' },
    { 'data': 'collection.label' },
    { 'data': 'resolution.name' },
    { 'data': 'scenario.name' },
    { 'data': 'data_kind.name' },
    { 'data': 'file_type.name' },
    { 'data': 'time_start' },
    { 'data': 'time_end' },
    { 'data': 'description' }
];

var dataset_columnsDefs = [
    { width: '20px', targets: 0, orderable: false, className: 'select-checkbox' },  // Select checkbox
    { width: '45px', targets: 1, orderable: false },  // Buttons
    { width: '5%', targets: 2 },  // Id
    { width: '45px', targets: 3,   // Is visible
      render: (data) => {
          return data == 0 ? "" : '<span class="glyphicon glyphicon-ok"></span>';
      }
    },
    { width: '11%', targets: 4 },  // Collection label
    { width: '10%', targets: 5 },  // Resolution
    { width: '15%', targets: 6 },  // Scenario
    { width: '7%', targets: 7 },   //Data kind
    { width: '7%', targets: 8 },   // File type
    { width: '8%', targets: 9 },  // Time start
    { width: '8%', targets: 10 },  // Time end
    { width: '15%', targets: 11 }  // Description
];

$(document).ready( function () {
    $('a[data-toggle="tab"]').on( 'shown.bs.tab', function() {
        columnsAdjust();
    } );
    $(window).resize(function () {
        columnsAdjust();
    });

    // Create Datasets table
    var datasetOptions = $.extend(true, {}, commonOptions);
    datasetOptions["columnDefs"] = dataset_columnsDefs.concat(all_columns_defs),
    datasetOptions["columns"] = dataset_columns;
    datasetOptions["ajax"] = { 'url': dataset_api_url, 'type': 'GET', 'dataSrc': 'data' };
    $('#main-tabs a[href="#tab-dataset"]').on('click', function() {
        if (!$.fn.DataTable.isDataTable('#dataset')) {
            $('#dataset').DataTable( datasetOptions ).on('draw', function() {
                addUpdDelButtonHandlers.call(this, 'dataset');
            });
            $('#dataset').DataTable().on('xhr.dt', set_header);
        }
    });
});
