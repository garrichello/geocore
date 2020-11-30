$(function() {
    var dataset_form_class_name = '.'+JSON.parse($('#dataset-form-class-name')[0].textContent);

    var loadCollections = function(form_name, collection_label='') {
        var form = $(form_name);
        var modal_id = '#'+getModalName(form.attr('action')); // Dataset modal!
        console.log('[loadCollections] modal_id: '+modal_id);

        $.ajax( {
            url: form.attr('collections-url'),
            type: 'get',
            success: function (data) {
                $(modal_id+' #id_collection').html(data);
                if (collection_label.length) {
                    $(modal_id+` #id_collection option:contains("${collection_label}")`).attr(
                        'selected', true);  // Select new collection in the select
                }
                if ($(modal_id+' #id_collection option').length == 2) {
                    $(modal_id+' #id_collection').prop("selectedIndex", 1);
                }
            }
        } );
    };

    var loadResolutions = function(form_name, resolution_name='') {
        var form = $(form_name);
        var modal_id = '#'+getModalName(form.attr('action')); // Dataset modal!

        $.ajax( {
            url: form.attr('resolutions-url'),
            type: 'get',
            success: function (data) {
                $(modal_id+' #id_resolution').html(data);
                if (resolution_name.length) {
                    $(modal_id+` #id_resolution option:contains("${resolution_name}")`).attr(
                        'selected', true);  // Select new collection in the select
                }
                if ($(modal_id+' #id_resolution option').length == 2) {
                    $(modal_id+' #id_resolution').prop("selectedIndex", 1);
                }
            }
        } );
    };

    var loadScenarios = function(form_name, scenario_name='') {
        var form = $(form_name);
        var modal_id = '#'+getModalName(form.attr('action')); // Dataset modal!

        $.ajax( {
            url: form.attr('scenarios-url'),
            type: 'get',
            success: function (data) {
                $(modal_id+' #id_scenario').html(data);
                $(modal_id+` #id_scenario option:contains("${scenario_name}")`).attr(
                    'selected', true);  // Select new collection in the select
                if ($(modal_id+' #id_scenario option').length == 2) {
                    $(modal_id+' #id_scenario').prop("selectedIndex", 1);
                }
            }
        } );
    };

    var loadDatakinds = function(form_name, datakind_name='') {
        var form = $(form_name);
        var modal_id = '#'+getModalName(form.attr('action')); // Dataset modal!

        $.ajax( {
            url: form.attr('datakinds-url'),
            type: 'get',
            success: function (data) {
                $(modal_id+' #id_data_kind').html(data);
                $(modal_id+` #id_data_kind option:contains("${datakind_name}")`).attr(
                    'selected', true);  // Select new collection in the select
                if ($(modal_id+' #id_data_kind option').length == 2) {
                    $(modal_id+' #id_data_kind').prop("selectedIndex", 1);
                }
            }
        } );
    };

    var loadFiletypes = function(form_name, filetype_name='') {
        var form = $(form_name);
        var modal_id = '#'+getModalName(form.attr('action')); // Dataset modal!

        $.ajax( {
            url: form.attr('filetypes-url'),
            type: 'get',
            success: function (data) {
                $(modal_id+' #id_file_type').html(data);
                $(modal_id+` #id_file_type option:contains("${filetype_name}")`).attr(
                    'selected', true);  // Select new collection in the select
                if ($(modal_id+' #id_file_type option').length == 2) {
                    $(modal_id+' #id_file_type').prop("selectedIndex", 1);
                }
            }
        } );
    };

    // Submit form
    $('body').on('submit', '.js-dataset-create-form', function(e) {
        saveForm2.call(this, e); return false;
    });

    // Create collection
    $(dataset_form_class_name).on('click', '.js-add-button', function() { 
        var modal_id = loadForm2.call(this);
        console.log('[Dataset click] Form '+dataset_form_class_name+'; Modal ID: '+modal_id);
        $(modal_id).on('hidden.bs.modal', function() {
            console.log('[Dataset hide] Form '+dataset_form_class_name+'; Modal ID: '+modal_id);
            if ($('.js-collection-create-form').length) {
                var form_data = mapFormData('.js-collection-create-form');  // Get collection fields
                loadCollections.call(this, dataset_form_class_name, form_data['label']);
                console.log('In dataset modal, form data: '+form_data['label']);
            };
            if ($('.js-resolution-create-form').length) {
                var form_data = mapFormData('.js-resolution-create-form');  // Get collection fields
                loadResolutions.call(this, dataset_form_class_name, form_data['name']);
                console.log('In dataset modal, form data: '+form_data['name']);
            };
            $(modal_id).remove();
        })
    });

    var resolution_form_class = '.js-resolution-create-form';
    $('body').on('submit', resolution_form_class, function(e) {
        saveForm2.call(this, e);
        var form_data = mapFormData(resolution_form_class);  // Get fields of the form as a map
        loadResolutions.call(this, dataset_form_class_name, form_data['name']);
        return false; 
    });

    var scenario_form_class = '.js-scenario-create-form';
    $('body').on('submit', scenario_form_class, function(e) {
        saveForm2.call(this, e);
        var form_data = mapFormData(scenario_form_class);  // Get fields of the form as a map
        loadScenarios.call(this, dataset_form_class_name, form_data['name']);
        return false; 
    });

    var datakind_form_class = '.js-datakind-create-form';
    $('body').on('submit', datakind_form_class, function(e) {
        saveForm2.call(this, e);
        var form_data = mapFormData(datakind_form_class);  // Get fields of the form as a map
        loadDatakinds.call(this, dataset_form_class_name, form_data['name']);
        return false; 
    });

    var filetype_form_class = '.js-filetype-create-form';
    $('body').on('submit', filetype_form_class, function(e) {
        saveForm2.call(this, e);
        var form_data = mapFormData(filetype_form_class);  // Get fields of the form as a map
        loadFiletypes.call(this, dataset_form_class_name, form_data['name']);
        return false; 
    });
});
