var form_class_name = '.'+JSON.parse($('#form-class-name')[0].textContent);

var loadCollections = function(form_name) {
    var form = $(form_name);

    $.ajax( {
        url: form.attr('collections-url'),
        type: 'get',
        success: function (data) {
            $('#modal-dataset #id_collection').html(data);
            if ($('#modal-dataset #id_collection option').length == 2) {
                $('#modal-dataset #id_collection').prop("selectedIndex", 1);
            }
        }
    } );
};

var loadResolutions = function(form_name) {
    var form = $(form_name);

    $.ajax( {
        url: form.attr('resolutions-url'),
        type: 'get',
        success: function (data) {
            $('#modal-dataset #id_resolution').html(data);
            if ($('#modal-dataset #id_resolution option').length == 2) {
                $('#modal-dataset #id_resolution').prop("selectedIndex", 1);
            }
        }
    } );
};

var loadScenarios = function(form_name) {
    var form = $(form_name);

    $.ajax( {
        url: form.attr('scenarios-url'),
        type: 'get',
        success: function (data) {
            $('#modal-dataset #id_scenario').html(data);
            if ($('#modal-dataset #id_scenario option').length == 2) {
                $('#modal-dataset #id_scenario').prop("selectedIndex", 1);
            }
        }
    } );
};

var loadDatakinds = function(form_name) {
    var form = $(form_name);

    $.ajax( {
        url: form.attr('datakinds-url'),
        type: 'get',
        success: function (data) {
            $('#modal-dataset #id_data_kind').html(data);
            if ($('#modal-dataset #id_data_kind option').length == 2) {
                $('#modal-dataset #id_data_kind').prop("selectedIndex", 1);
            }
        }
    } );
};

var loadFiletypes = function(form_name) {
    var form = $(form_name);

    $.ajax( {
        url: form.attr('filetypes-url'),
        type: 'get',
        success: function (data) {
            $('#modal-dataset #id_file_type').html(data);
            if ($('#modal-dataset #id_file_type option').length == 2) {
                $('#modal-dataset #id_file_type').prop("selectedIndex", 1);
            }
        }
    } );
};

$('#modal-over').on('submit', '.js-collection-create-form', function(e) {
    saveForm.call(this, e, '#modal-over');
    loadCollections.call(this, form_class_name);
    return false; 
});

$('#modal-over').on('submit', '.js-resolution-create-form', function(e) {
    saveForm.call(this, e, '#modal-over');
    loadResolutions.call(this, form_class_name);
    return false; 
});

$('#modal-over').on('submit', '.js-scenario-create-form', function(e) {
    saveForm.call(this, e, '#modal-over');
    loadScenarios.call(this, form_class_name);
    return false; 
});

$('#modal-over').on('submit', '.js-datakind-create-form', function(e) {
    saveForm.call(this, e, '#modal-over');
    loadDatakinds.call(this, form_class_name);
    return false; 
});

$('#modal-over').on('submit', '.js-filetype-create-form', function(e) {
    saveForm.call(this, e, '#modal-over');
    loadFiletypes.call(this, form_class_name);
    return false; 
});
