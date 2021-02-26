var conveyor_api_url = $('#tab-conveyor').attr('api-data-url')

function set_header2(e, settings, json, xhr) {
    // Get headers from JSON data and put them into the table
    var table = $(this).DataTable();

    if (json != null) {
        $.each(json.headers, function(i, v) {
            table.columns().header()[i+1].innerText = v.caption;  // Start at the 3rd column
            $(table.columns().header()[i+1]).addClass(v.type);
        })
    }
}

conveyor_columns = [
    { 'render': function (data, type, row, meta) {
        return '<div><button type="button" class="btn btn-warning btn-sm js-update-conveyor"'
               + `data-url="${conveyor_api_url}${row.id}/">`
               + '<span class="glyphicon glyphicon-pencil"></span></button></div>&nbsp;'
               + '<div><button type="button" class="btn btn-danger btn-sm js-delete-conveyor"'
               + `data-url="${conveyor_api_url}${row.id}/">`
               + '<span class="glyphicon glyphicon-trash"></span></button></div>';
    } },  // for buttons
    { 'data': 'id' },
    { 'data': 'label' },
]

conveyor_columnsDefs = [
    { width: '45px', targets: 0, orderable: false, }, // Buttons
    { width: '20%', targets: 1 },  // Id
    { width: '75%', targets: 2 },  // Label
]

var loadGraph = function(url) {
    $.ajax({
        type: "get",
        url: url,
        dataType: 'json',
        success: function(data) {
            console.log(data);
            return data;
        },
        error: function(xhr, errmsg, err) {
            console.error('Error occured when loading graph data');
            return {};
        }
    });
};

$(document).ready( function () {
    // Create conveyors table
    var conveyorOptions = $.extend(true, {}, commonOptions);
    conveyorOptions["columnDefs"] = conveyor_columnsDefs.concat(all_columns_defs);
    conveyorOptions["columns"] = conveyor_columns;
    conveyorOptions["select"] = {style: 'single',},
    conveyorOptions["order"] = [[ 1, 'asc' ]],
    conveyorOptions["ajax"] = { 'url': conveyor_api_url, 'type': 'GET', 'dataSrc': 'data' };
    $('#main-tabs a[href="#tab-conveyor"]').on('click', function() {
        if (!$.fn.DataTable.isDataTable('#conveyor')) {
            $('#conveyor').DataTable( conveyorOptions ).on('draw', function() {
                addUpdDelButtonHandlers.call(this, 'conveyor');
            });
            var table = $('#conveyor').DataTable();
            table.on('xhr.dt', set_header2);
            table.on('select', function( e, dt, type, indexes ) {
                if (type == 'row') {
                    var url = table.rows(indexes).data().pluck('dataurl')[0]+'graph/';
                    $.ajax({
                        type: "get",
                        url: url,
                        dataType: 'json',
                        success: function(data) {
                            $flowchart.flowchart('setData', data);
                        },
                        error: function(xhr, errmsg, err) {
                            console.error('Error occured when loading graph data');
                        }
                    });              
                }
            });
        }
    });

    // Create graph container
    var $flowchart = $('#flowchartworkspace');
    var $container = $flowchart.parent();

    // Apply the plugin on a standard, empty div...
    $flowchart.flowchart({
        data: {},
        linkWidth: 3,
        distanceFromArrow: 0,
        defaultSelectedLinkColor: '#000055',
        grid: 10,
        multipleLinksOnInput: true,
        multipleLinksOnOutput: true,
        canUserEditLinks: false,
    });

} );