$(document).ready( function () {
    // Create Specific parameter table
    var apiURL = $('#tab-specpar').attr('api-data-url');

    var specpar_columns = [
        {'render': function() { return null; }}, // For checkboxes
        {'render': function(data, type, row, meta) {
            return renderButtons(row, apiURL)
        }},  // for buttons
        {'data': 'id'},
        {'data': 'parameter.is_visible'},
        {'data': 'parameter.parameteri18n.name'},
        {'data': 'parameter.accumulation_mode.name'},
        {'data': 'time_step.timestepi18n.name'},
        {'data': 'time_step.label'},
        {'data': 'time_step.subpath2'},
        {'data': 'levels_group.units.unitsi18n.name'},
        {'data': 'levels_group.description'},
        {'data': function(data, type, row, meta) {
            var levels = [];
            data.levels_group.levels.forEach((element) => {
                levels.push(element.leveli18n.name);
            });
            return levels.join();
        } }
    ];
    
    var specpar_columnsDefs = [
        { width: '20px', targets: 0, orderable: false, className: 'select-checkbox' },  // Select checkbox
        { width: '45px', targets: 1, orderable: false },  // Buttons
        { width: '25px', targets: 2 },  // Id
        { width: '45px', targets: 3,   // Is visible
          render: function(data) {
              return data == 0 ? "" : '<span class="glyphicon glyphicon-ok"></span>';
          }
        },
        { width: '195px', targets: 4 },   // Parameter name
        { width: '95px', targets: 5 },   // Accumulation mode
        { width: '95px', targets: 6 },   // Time step name
        { width: '55px', targets: 7 },   // Time step label
        { width: '75px', targets: 8 },   // Time step subpath
        { width: '95px', targets: 9 },   // Levels group
        { width: '95px', targets: 10 },  // Levels group description
        { width: '175px', targets: 11 }  // Levels
    ];

    var specparOptions = $.extend(true, {}, commonOptions);
    specparOptions["columnDefs"] = specpar_columnsDefs.concat(all_columns_defs),
    specparOptions["columns"] = specpar_columns;
    specparOptions["ajax"] = { 'url': apiURL, 'type': 'GET', 'dataSrc': 'data' };
    $('#main-tabs a[href="#tab-specpar"]').on('click', function() {
        if (!$.fn.DataTable.isDataTable('#specpar')) {
            $('#specpar').DataTable( specparOptions ).on('draw', function() {
                addUpdDelButtonHandlers.call(this, 'specpar');
            });
            $('#specpar').DataTable().on('xhr.dt', set_header);
        }
    });
});
