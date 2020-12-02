$(function() {
    var dataset_form_class_name = '.'+JSON.parse($('#dataset-form-class-name')[0].textContent);

    var loadCollections = function(form_name, collection_label='') {
        var form = $(form_name);
        var modal_id = '#'+getModalName(form.attr('action'));

        if (collection_label.length) {
            $.ajax( {
                url: form.attr('collections-url'),
                type: 'get',
                success: function(data) {
                    $(modal_id+' #id_collection').html(data);
                    $(modal_id+` #id_collection option:contains("${collection_label}")`).attr(
                        'selected', true);  // Select new collection in the select
                    if ($(modal_id+' #id_collection option').length == 2) {
                        $(modal_id+' #id_collection').prop("selectedIndex", 1);
                    }
                },
            } );
        }
    };

    var loadResolutions = function(form_name, resolution_name='') {
        var form = $(form_name);
        var modal_id = '#'+getModalName(form.attr('action'));

        if (resolution_name.length) {
            $.ajax( {
                url: form.attr('resolutions-url'),
                type: 'get',
                success: function(data) {
                    $(modal_id+' #id_resolution').html(data);
                        $(modal_id+` #id_resolution option:contains("${resolution_name}")`).attr(
                            'selected', true);  // Select new resolution in the select
                    if ($(modal_id+' #id_resolution option').length == 2) {
                        $(modal_id+' #id_resolution').prop("selectedIndex", 1);
                    }
                }
            } );
        }
    };

    var loadScenarios = function(form_name, scenario_name='') {
        var form = $(form_name);
        var modal_id = '#'+getModalName(form.attr('action'));

        if (scenario_name.length) {
            $.ajax( {
                url: form.attr('scenarios-url'),
                type: 'get',
                success: function (data) {
                    $(modal_id+' #id_scenario').html(data);
                    $(modal_id+` #id_scenario option:contains("${scenario_name}")`).attr(
                        'selected', true);  // Select new scenario in the select
                    if ($(modal_id+' #id_scenario option').length == 2) {
                        $(modal_id+' #id_scenario').prop("selectedIndex", 1);
                    }
                }
            } );
        }
    };

    var loadDatakinds = function(form_name, datakind_name='') {
        var form = $(form_name);
        var modal_id = '#'+getModalName(form.attr('action'));

        if (datakind_name.length) {
            $.ajax( {
                url: form.attr('datakinds-url'),
                type: 'get',
                success: function (data) {
                    $(modal_id+' #id_data_kind').html(data);
                    $(modal_id+` #id_data_kind option:contains("${datakind_name}")`).attr(
                        'selected', true);  // Select new datakind in the select
                    if ($(modal_id+' #id_data_kind option').length == 2) {
                        $(modal_id+' #id_data_kind').prop("selectedIndex", 1);
                    }
                }
            } );
        }
    };

    var loadFiletypes = function(form_name, filetype_name='') {
        var form = $(form_name);
        var modal_id = '#'+getModalName(form.attr('action'));

        if (filetype_name.length) {
            $.ajax( {
                url: form.attr('filetypes-url'),
                type: 'get',
                success: function (data) {
                    $(modal_id+' #id_file_type').html(data);
                    $(modal_id+` #id_file_type option:contains("${filetype_name}")`).attr(
                        'selected', true);  // Select new filetype in the select
                    if ($(modal_id+' #id_file_type option').length == 2) {
                        $(modal_id+' #id_file_type').prop("selectedIndex", 1);
                    }
                }
            } );
        }
    };
    
    // Submit form
    $('body').on('submit', '.js-dataset-create-form', function(e) {
        saveForm2.call(this, e); return false;
    });

    // + buttons handling
    $(dataset_form_class_name).on('click', '.js-add-button', function() { 
        var modal_id = loadForm2.call(this);
        $(modal_id).on('hidden.bs.modal', function() {
            if ($('.js-collection-create-form').length) {
                var form_data = mapFormData('.js-collection-create-form');  // Get collection fields
                loadCollections.call(this, dataset_form_class_name, form_data['label']);
            };
            if ($('.js-resolution-create-form').length) {
                var form_data = mapFormData('.js-resolution-create-form');  // Get resolution fields
                loadResolutions.call(this, dataset_form_class_name, form_data['name']);
            };
            if ($('.js-scenario-create-form').length) {
                var form_data = mapFormData('.js-scenario-create-form');  // Get scenario fields
                loadScenarios.call(this, dataset_form_class_name, form_data['name']);
            };
            if ($('.js-datakind-create-form').length) {
                var form_data = mapFormData('.js-datakind-create-form');  // Get datakind fields
                loadDatakinds.call(this, dataset_form_class_name, form_data['name']);
            };
            if ($('.js-filetype-create-form').length) {
                var form_data = mapFormData('.js-filetype-create-form');  // Get filetype fields
                loadFiletypes.call(this, dataset_form_class_name, form_data['name']);
            };
            $(modal_id).remove();
        })
    });
});
