var data_api_url = $('#tab-data').attr('api-data-url');

var data_columns = [
    { 'render': function() { return null; } }, // For checkboxes
    { 'render': function (data, type, row, meta) {
        return '<div><button type="button" class="btn btn-warning btn-sm js-update-data"'
               + `data-url="${data_api_url}${row.id}">`
               + '<span class="glyphicon glyphicon-pencil"></span></button></div>&nbsp;'
               + '<div><button type="button" class="btn btn-danger btn-sm js-delete-data"'
               + `data-url="${data_api_url}${row.id}">`
               + '<span class="glyphicon glyphicon-trash"></span></button></div>';
    } },
    { 'data': 'id' },
    { 'data': 'dataset.is_visible' },
    { 'data': 'dataset.collection.label' },
    { 'data': 'dataset.resolution.name' },
    { 'data': 'dataset.scenario.name' },
    { 'data': 'parameter.is_visible' },
    { 'data': 'parameter.parameteri18n.name' },
    { 'data': 'time_step.timestepi18n.name' },
    { 'data': 'levels_group.description' },
    { 'data': function(data, type, row, meta) {
        var levels = [];
        data.levels_group.levels.forEach((element) => {
            levels.push(element.leveli18n.name);
        });
        return levels.join();
    } },
    { 'data': 'levels_variable.name' },
    { 'data': 'variable.name' },
    { 'data': 'units.unitsi18n.name' },
    { 'data': 'property.label' },
    { 'data': 'property_value.label' },
    { 'data': 'root_dir.name' },
    { 'data': 'dataset.scenario.subpath0' },
    { 'data': 'dataset.resolution.subpath1' },
    { 'data': 'time_step.subpath2' },
    { 'data': 'file.name_pattern' },
    { 'data': 'scale' },
    { 'data': 'offset' }
];

var data_columnsDefs = [
    { width: '20px', targets: 0, orderable: false, className: 'select-checkbox' },  // Select checkbox
    { width: '45px', targets: 1, orderable: false },  // Buttons
    { width: '25px', targets: 2 },    // Id
    { width: '55px', targets: 3,   // Is dataset visible
      render: (data) => {
          return data == 0 ? "" : '<span class="glyphicon glyphicon-ok"></span>';
      }
    },
    { width: '95px', targets: 4 },   // Collection label
    { width: '75px', targets: 5 },    // Resolution
    { width: '95px', targets: 6 },    // Scenario
    { width: '65px', targets: 7,   // Is parameter visible
      render: (data) => {
          return data == 0 ? "" : '<span class="glyphicon glyphicon-ok"></span>';
      }
    },
    { width: '95px', targets: 8 },    // Parameter
    { width: '75px', targets: 9 },    // Time step
    { width: '95px', targets: 10 },   // Levels group
    { width: '175px', targets: 11 },  // Levels names
    { width: '55px', targets: 12 },   // Levels variable
    { width: '95px', targets: 13 },    // Variable name
    { width: '55px', targets: 14 },   // Units
    { width: '85px', targets: 15 },   // Property label
    { width: '85px', targets: 16 },   // Property value
    { width: '165px', targets: 17 },   // Root dir
    { width: '75px', targets: 18 },   // Subpath0
    { width: '75px', targets: 19 },   // Subpath1
    { width: '75px', targets: 20 },   // Subpath2
    { width: '165px', targets: 21 },  // File pattern
    { width: '55px', targets: 22 },   // Scale
    { width: '55px', targets: 23 }   // Offset
];

$(document).ready( function () {
// Create Data table
    var dataOptions = $.extend(true, {}, commonOptions);
    dataOptions["columnDefs"] = data_columnsDefs.concat(all_columns_defs),
    dataOptions["columns"] = data_columns;
    dataOptions["ajax"] = { 'url': data_api_url, 'type': 'GET', 'dataSrc': 'data' };
    $('#main-tabs a[href="#tab-data"]').on('click', function() {
        if (!$.fn.DataTable.isDataTable('#data')) {
            $('#data').DataTable( dataOptions ).on('draw', function() {
                addUpdDelButtonHandlers.call(this, 'data');
            });
            $('#data').DataTable().on('xhr.dt', set_header);
        }
    });
});
