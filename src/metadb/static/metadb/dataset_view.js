$(document).ready( function () {
    // Create Datasets table
    var apiURL = $('#tab-dataset').attr('api-data-url');

    var dataset_columns = [
        {'render': function() { return null; }}, // For checkboxes
        {'render': (data, type, row, meta) => {
            return renderButtons(row, apiURL)
        }},  // for buttons
        {'data': 'id'},
        {'data': 'is_visible'},
        {'data': 'collection.label'},
        {'data': 'resolution.name'},
        {'data': 'scenario.name'},
        {'data': 'data_kind.name'},
        {'data': 'file_type.name'},
        {'data': 'time_start'},
        {'data': 'time_end'},
        {'data': 'description'}
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

    var datasetOptions = $.extend(true, {}, commonOptions);
    datasetOptions["columnDefs"] = dataset_columnsDefs.concat(all_columns_defs),
    datasetOptions["columns"] = dataset_columns;
    datasetOptions["ajax"] = { 'url': apiURL, 'type': 'GET', 'dataSrc': 'data' };
    $('#main-tabs a[href="#tab-dataset"]').on('click', function() {
        if (!$.fn.DataTable.isDataTable('#dataset')) {
            $('#dataset').DataTable( datasetOptions ).on('draw', function() {
                addUpdDelButtonHandlers.call(this, 'dataset');
            });
            $('#dataset').DataTable().on('xhr.dt', set_header);
        }
    });
});
