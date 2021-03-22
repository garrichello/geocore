var processor_api_url = $('#tab-processor').attr('api-data-url')

processor_columns = [
    { 'render': function() { return null; } },  // For checkboxes
    { 'render': function (data, type, row, meta) {
        return '<div><button type="button" class="btn btn-warning btn-sm js-update-processor"'
               + `data-url="${processor_api_url}${row.id}">`
               + '<span class="glyphicon glyphicon-pencil"></span></button></div>&nbsp;'
               + '<div><button type="button" class="btn btn-danger btn-sm js-delete-processor"'
               + `data-url="${processor_api_url}${row.id}">`
               + '<span class="glyphicon glyphicon-trash"></span></button></div>';
    } },  // for buttons
    { 'data': 'id' },
    { 'data': 'is_visible' },
    { 'data': 'processori18n.name' },
    { 'data': 'processori18n.description' },
    { 'data': 'processori18n.reference' },
    { 'data': 'conveyor.label' },
    { 'data': (data, type, row, meta) => {
        labels = Array();
        data.settings.forEach(element => {
            labels.push(element.label);
        });
        return labels.join(';<br>');
    } },
    { 'data': (data, type, row, meta) => {
        names = Array();
        data.time_period_types.forEach(element => {
            names.push(element.timeperiodtypei18n.name);
        });
        return names.join(';<br>');
    } },
    { 'data': 'arguments_selected_by_user' },
    { 'data': (data, type, row, meta) => {
        var arguments = Array();
        data.arguments.forEach(element => {
            var pos = element.argument_position;
            var name = element.arguments_group.name;
            var type = element.arguments_group.argument_type.label;
            arguments.push(`Input ${pos}: ${name} (${type})`);
        });
        arguments.sort();
        return arguments.join(';<br>');
    } },
]

processor_columnsDefs = [
    { width: '20px', targets: 0, orderable: false, className: 'select-checkbox' }, // Select checkbox
    { width: '45px', targets: 1, orderable: false, }, // Buttons
    { width: '65px', targets: 2, },   // id
    { width: '55px', targets: 3,      // is visible
        render: (data) => {
            return data == 0 ? "" : '<span class="glyphicon glyphicon-ok"></span>';
        },
    },
    { width: '155px', targets: 4 },    // processor name
    { width: '215px', targets: 5 },   // processor description
    { width: '175px', targets: 6,     // processor reference
        render: (data) => {
            return data == null ? "" : `<a href="${data}" target="_blank">${data}</a>`;
        },
    },
    { width: '175px', targets: 7 },    // conveyor label
    { width: '125px', targets: 8 },    // settings
    { width: '125px', targets: 9 },    // time period types
    { width: '75px', targets: 10 },  // arguments selected by user
    { width: '185px', targets: 11 },   // arguments
]

function format(data) {
    var settings = '<tr>'+data.data.label+'</tr>';
    data.data.combinations.forEach(element => {
        var comb = element.index+': '+element.combination.option.label+' = '+element.combination.option_value.optionvaluei18n.name;
        var cond = '';
        if (element.combination.condition.option.label != '-') {
            cond = ' [if '+element.combination.condition.option.label+' == '+element.combination.condition.option_value.optionvaluei18n.name+']';
        };
        console.log(' '+comb+cond);
    });
    return settings;
}

function showDetails(row) {
    var data = row.data();
    
    $.ajax({
        type: "get",
        headers: {
            'ACTION': 'json',
        },
        url: data.fulldataurl,  // get full info of the selected processor
        dataType: 'json',
        beforeSend: () => {
            $('#processor_processing').show();
        },
        complete: () => {
            $('#processor_processing').hide();        },
        success: (data) => {
            var settingsText = '';
            data.data.settings.forEach(setting => {
                settingsText += '<tr><td>'+setting.label+' = { ';
                var combinationsText = Array();
                setting.combinations.forEach(element => {
                    var comb = element.index+': '+element.combination.option.label+'='+element.combination.option_value.label;
                    var cond = '';
                    if (element.combination.condition.option.label != '-') {
                        cond = ' | '+element.combination.condition.option.label+'=='+element.combination.condition.option_value.label;
                    };
                    combinationsText.push(comb + cond);
                });
                settingsText = settingsText + combinationsText.join(', ') + ' }</td></tr>';
            });
            var argumentsText = '';
            data.data.arguments.forEach(argument => {
                argumentsText += '<tr><td> Input '+argument.argument_position+': '+argument.arguments_group.name+
                                 ' ('+argument.arguments_group.argument_type.label+') = [ ';
                var specparsText = Array();
                argument.arguments_group.specific_parameter.forEach(specpar => {
                    var text = specpar.parameter.parameteri18n.name+' every '+
                               specpar.time_step.timestepi18n.name+' at '+
                               specpar.levels_group.description;
                    specparsText.push(text);
                });
                var processorsText = Array();
                argument.arguments_group.processors.forEach(processor => {
                    var text = processor.processor.processori18n.name;
                    processorsText.push(text);
                });
                argumentsText += specparsText.join('; ')+processorsText.join('; ')+' ]</td></tr>';
            });

            var details = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
                '<tr>'+
                    '<td><b>Settings:</b></td>'+
                '</tr>'+
                settingsText+
                '<tr>'+
                    '<td><b>Arguments:</b></td>'+
                '</tr>'+
                argumentsText+
                '</table>';
            row.child( details ).show();
        },
    });
}

$(document).ready( function () {
    // Create processor table
    var processorOptions = $.extend(true, {}, commonOptions);
    processorOptions["columnDefs"] = processor_columnsDefs.concat(all_columns_defs);
    processorOptions["columns"] = processor_columns;
    processorOptions["ajax"] = { 'url': processor_api_url, 'type': 'GET', 'dataSrc': 'data' };
    $('#main-tabs a[href="#tab-processor"]').on('click', function() {
        if (!$.fn.DataTable.isDataTable('#processor')) {
            var table = $('#processor').DataTable( processorOptions );
            table.on('draw', function() {
                addUpdDelButtonHandlers.call(this, 'processor');
            });
            table.on('xhr.dt', set_header);
            $('#processor').on('click', 'tr', (e) => {
                var tr = $(e.currentTarget);
                var row = table.row(tr);

                if ( row.child.isShown() ) {
                    // This row is already open - close it
                    row.child.hide();
                    tr.removeClass('shown');
                }
                else {
                    // Open this row
                    showDetails(row);
                    tr.addClass('shown');
                }
            });
        }
    });
})
