$(document).ready( function () {
    // Create Other tables
    var apiURL;
    var otherOptions = {
        sDom: 'tri',
        orderCellsTop: true,
        paginate: false,
        select: {style: 'multi', selector: 'td:first-child',},
        scrollY: 400,
        scrollX: true,
        scrollCollapse: true,
        order: [[ 2, 'dsc' ]],
        processing: true,
        autoWidth: true,
        language: {
            'loadingRecords': '&nbsp',
            'processing': '<div class="spinner"></div>'
        }
    };

    function prePostInit(table, headers) {
        instance = table.settings()[0].oInstance;
        for (var i = 2; i < table.columns().header().length; i++) {
            $(table.columns(i).header()).addClass(headers[i-2].type);
        }
        postInit.call(instance);
    }
    
    function dwell(dict, path) {
        var val = dict;
        chunks = path.split('.');
        $.each(chunks, (i, chunk) => {
            val = val[chunk];
        });
        return val;
    }
    
    function delister(data, field_idx) {
        // Here we extract items from an Array of dictionaries came from the server as a JSON.
        // In rare cases a field contains a LIST of structures (dictionaries) with items.
        // Items can be borrowed deep in the nested dictionary structure.
        // subfield field in the JSON helps to reach for these items.
        $.each(data.data, (i, e) => {  // loop over rows
            $.each(e, (v, k) => {  // loop over columns
                if (Array.isArray(k)) {  // if a cell contains an Array
                    var items = Array();  // here we will store the Array items
                    $.each(data.data[i][v], (l, m) => {  // loop over items
                        items.push(dwell(m, data.headers[field_idx[v]].subfield));  // group
                    });
                    if (items.length == 0) {  // Empty array replaced with '-'-value
                        items[0] = '-';
                    };
                    data.data[i][v] = items.join(';<br>'); // replace original dict with the array
                };
            })
        });
    }
    
    function create_dt(data, data_url) {
        if ($.fn.DataTable.isDataTable('#other')) {
            $('#other').DataTable().destroy();
            $('#other').empty();
            $('#other').off();
        }
        var columns = [
            {'render': function() { return null; }},  // For checkboxes
            {'render': (data, type, row, meta) => {
                return renderButtons(row, apiURL)
            }}  // for buttons
        ];
        var field_idx = [];
        $.each(data.headers, function (i, v) {
            columns.push({data: v.field, title: v.caption}); // describe columns headers
            field_idx[v.field] = i;  // map field name to its column position
        });
        delister(data, field_idx);
        otherOptions['data'] = data.data;
        otherOptions['columns'] = columns;
        otherOptions['columnDefs'] = [
            { width: 20, targets: 0, orderable: false, className: 'select-checkbox' }, // Select checkbox
            { width: 45, targets: 1, orderable: false, }, // Buttons
        ]
        var odt = $('#other').DataTable( otherOptions );
        prePostInit(odt, data.headers);
        odt.on('draw', function() {
            addUpdDelButtonHandlers.call(this, 'other');
        });
        odt.on('processing', function(e, settings, procesing) {
            if (typeof processing !== 'undefined') {
                $('#other_processing').css( 'display', processing ? 'block' : 'none' );
            };
        })
        odt.on('xhr', (e, settings, json, xhr) => {
            delister(json, field_idx);
        })
        addUpdDelButtonHandlers('other');
        odt.ajax.url(data_url);
    }
    
    function get_data(data_url) {
        $.ajax({
            url: data_url,
            dataType: 'json',
            beforeSend: function() {
                $('#other_processing').show();
            },
            success: function(data) {
                create_dt(data, data_url);
                $('#other_processing').hide();
            }
        });
    }

    // Add button
    $('.js-data-choice').click(function() {
        apiURL = $(this).attr('api-data-url');
        get_data.call(this, apiURL);
        $('.js-create').attr('data-url', $(this).attr('create-data-url'));
    });

    // Other tab
    $('#main-tabs a[href="#tab-other"]').on('click', function() {
        $('.js-data-choice[checked=checked]').trigger('click');
    });

} );