function loadGraph(url, $flowchart) {
    $.ajax({
        type: "get",
        headers: {
            'ACTION': 'graph'
        },
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

$(document).ready( function () {
    "use strict";
    // Create graph container
    var apiURL = $('#tab-conveyor').attr('api-data-url');

    function set_header2(e, settings, json, xhr) {
        // Get headers from JSON data and put them into the table
        var table = $(this).DataTable();

        if (json != null) {
            $.each(json.headers, function(i, v) {
                table.columns().header()[i+1].innerText = v.caption;  // Start at the 3rd column
                $(table.columns().header()[i+1]).addClass(v.type);
            });
        }
    }

    var conveyor_columns = [
        {'render': function(data, type, row, meta) {
            return renderButtons(row, apiURL);
        }},  // for buttons
        {'data': 'id'},
        {'data': 'label'}
    ];

    var conveyor_columnsDefs = [
        { width: '45px', targets: 0, orderable: false }, // Buttons
        { width: '20%', targets: 1 },  // Id
        { width: '75%', targets: 2 }  // Label
    ];


    var $flowchart = $('#conveyor_preview');

    // Create conveyors table
    var conveyorOptions = $.extend(true, {}, commonOptions);
    conveyorOptions.columnDefs = conveyor_columnsDefs.concat(all_columns_defs);
    conveyorOptions.columns = conveyor_columns;
    conveyorOptions.select = {style: 'single'};
    conveyorOptions.order = [[ 1, 'asc' ]];
    conveyorOptions.ajax = { 'url': apiURL, 'type': 'GET', 'dataSrc': 'data' };
    $('#main-tabs a[href="#tab-conveyor"]').on('click', function() {
        if (!$.fn.DataTable.isDataTable('#conveyor')) {
            $('#conveyor').DataTable( conveyorOptions ).on('draw', function() {
                addUpdDelButtonHandlers.call(this, 'conveyor');
                $flowchart.flowchart('setData', {});
            });
            var table = $('#conveyor').DataTable();
            table.on('xhr.dt', set_header2);
            table.on('select', function( e, dt, type, indexes ) {
                if (type == 'row') {
                    var url = table.rows(indexes).data().pluck('dataurl')[0];
                    loadGraph(url, $flowchart);
                }
            });
        }
    });

    // Apply the plugin on a standard, empty div...
    $flowchart.flowchart({
        data: {},
        linkWidth: 3,
        distanceFromArrow: 0,
        defaultSelectedLinkColor: '#000055',
        grid: 10,
        multipleLinksOnInput: true,
        multipleLinksOnOutput: true,
        canUserEditLinks: false
    });
})