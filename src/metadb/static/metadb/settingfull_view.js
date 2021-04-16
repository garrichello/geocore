$(document).ready( function () {
    // Create setting table
    var apiURL = $('#tab-setting').attr('api-data-url')

    var setting_columns = [
        {'render': function() { return null; } },  // For checkboxes
        {'render': (data, type, row, meta) => {
            return renderButtons(row, apiURL)
        }},  // for buttons
        {'data': 'id' },
        {'data': 'label' },
        {'data': 'gui_element.name' },
        {'data': (data, type, row, meta) => {
            var combinations = Array();
            data.combinations.forEach(element => {
                var index = element.index;
                var name = element.combination.string;
                combinations.push(`${index}: ${name}`);
            });
            combinations.sort();
            return combinations.join(';<br>');
        }}
    ];
    
    var setting_columnsDefs = [
        { width: '20px', targets: 0, orderable: false, className: 'select-checkbox' }, // Select checkbox
        { width: '45px', targets: 1, orderable: false, }, // Buttons
        { width: '45px', targets: 2, },  // id
        { width: '95px', targets: 3 },   // label
        { width: '65px', targets: 4 },   // gui element name
        { width: '125px', targets: 5 }    // combinations
    ]
        
    var settingOptions = $.extend(true, {}, commonOptions);
    settingOptions["columnDefs"] = setting_columnsDefs.concat(all_columns_defs);
    settingOptions["columns"] = setting_columns;
    settingOptions["ajax"] = { 'url': apiURL, 'type': 'GET', 'dataSrc': 'data' };

    $('#main-tabs a[href="#tab-setting"]').on('click', function() {
        if (!$.fn.DataTable.isDataTable('#setting')) {
            var table = $('#setting').DataTable( settingOptions );
            table.on('draw', function() {
                addUpdDelButtonHandlers.call(this, 'setting');
            });
            table.on('xhr.dt', set_header);
        }
    });
})
