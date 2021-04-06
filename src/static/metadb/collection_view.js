$(document).ready( function () {
    // Create Collections table
    var apiURL = $('#tab-collection').attr('api-data-url');

    var collection_columns = [
        {'render': function() {
            return null;
        } },  // For checkboxes
        {'render': function(data, type, row, meta) {
            return renderButtons(row, apiURL)
        }},  // for buttons
        {'data': 'id'},
        {'data': 'label'},
        {'data': 'collectioni18n.name'},
        {'data': 'collectioni18n.description'},
        {'data': 'organization.organizationi18n.name'},
        {'data': 'organization.url'},
        {'data': 'url'}
    ];

    var collection_columnsDefs = [
        {width: '20px', targets: 0, orderable: false, className: 'select-checkbox'}, // Select checkbox
        {width: '45px', targets: 1, orderable: false}, // Buttons
        {width: '5%', targets: 2},  // Id
        {width: '11%', targets: 3},  // Label
        {width: '14%', targets: 4},  // Name
        {width: '20%', targets: 5},  // Description
        {width: '12%', targets: 6},  // Organization
        {width: '15%', targets: 7,  // Urganization URL
          render: (data) => `<a href="${data}" target="_blank">${data}</a>`
        },
        {width: '15%', targets: 8,  // URL
          render: (data) => `<a href="${data}" target="_blank">${data}</a>`
        }
    ];

    var collectionOptions = $.extend(true, {}, commonOptions);
    collectionOptions["columnDefs"] = collection_columnsDefs.concat(all_columns_defs);
    collectionOptions["columns"] = collection_columns;
    collectionOptions["ajax"] = { 'url': apiURL, 'type': 'GET', 'dataSrc': 'data' };
    $('#collection').DataTable( collectionOptions ).on('draw', function() {
        addUpdDelButtonHandlers.call(this, 'collection');
    });
    $('#collection').DataTable().on('xhr.dt', set_header);
});
