$(function () {
    var data_form_class_name = '.js-data-form';
    var modal_id = '#'+getModalName();

    var loadScenariosChain = function(form_name) {
        var form = $(form_name);
        var collectionId = $(modal_id+' #id_collection').val();
        var resolutionId = $(modal_id+' #id_resolution').val();
    
        $.ajax( {
            url: form.attr('dataset-scenario-url'),  // given a dataset get scenarios
            type: 'get',
            data: {
                'collectionId': collectionId,
                'resolutionId': resolutionId,
            },
            success: function (data) {
                $(modal_id+' #id_scenario').html(data);
                if ($(modal_id+' #id_scenario option').length == 2) {
                    $(modal_id+' #id_scenario').prop("selectedIndex", 1);
                }
            }
        } );
    };
    
    var loadResolutionsChain = function(form_name) {
        var form = $(form_name);
        var collectionId = $(modal_id+' #id_collection').val();
    
        $.ajax( {
            url: form.attr('dataset-resolutions-url'),  // given a dataset get resolutions
            type: 'get',
            data: {
                'collectionId': collectionId,
            },
            success: function (data) {
                $(modal_id+' #id_resolution').html(data);
                if ($(modal_id+' #id_resolution option').length == 2) {
                    $(modal_id+' #id_resolution').prop("selectedIndex", 1);
                }
                $(modal_id+' #id_resolution').trigger('change');
            }
        } );
    };
    
    var loadLvsGroupsChain = function(form_name) {
        var form = $(form_name);
        var parameteri18nId = $(modal_id+' #id_parameteri18n').val();
        var timestepi18nId = $(modal_id+' #id_time_stepi18n').val();
    
        $.ajax( {
            url: form.attr('parameter-lvsgroups-url'), // given a parameter load lvsgroups
            type: 'get',
            data: {
                'parameteri18nId': parameteri18nId,
                'timestepi18nId': timestepi18nId,
            },
            success: function (data) {
                $(modal_id+' #id_levels_group').html(data);
                if ($(modal_id+' #id_levels_group option').length == 2) {
                    $(modal_id+' #id_levels_group').prop("selectedIndex", 1);
                }
                $(modal_id+' #id_levels_group').trigger('change');
            }
        } );
    };
    
    var loadTimeStepsChain = function(form_name) {
        var form = $(form_name);
        var parameteri18nId = $(modal_id+' #id_parameteri18n').val();
    
        $.ajax( {
            url: form.attr('parameter-timesteps-url'), // given parameter load timesteps
            type: 'get',
            data: {
                'parameteri18nId': parameteri18nId,
            },
            success: function (data) {
                $(modal_id+' #id_time_stepi18n').html(data);
                if ($(modal_id+' #id_time_stepi18n option').length == 2) {
                    $(modal_id+' #id_time_stepi18n').prop("selectedIndex", 1);
                }
                $(modal_id+' #id_time_stepi18n').trigger('change');
            }
        } );
    };
    
    var loadLvsNamesChain = function(form_name) {
        var form = $(form_name);
        var lvsgroupId = $(modal_id+' #id_levels_group').val();
    
        $.ajax( { 
            url: form.attr('lvsgroup-lvsnames-url'),  // given a levels group load lvsnames
            type: 'get',
            data: {
                'lvsgroupId': lvsgroupId,
            },
            success: function (data) {
                $(modal_id+' #id_levels_namesi18n').val(data);
            }
        } );
    };
    
    var switchLvsVariable = function() {
        if ($(this).is(':checked')) {
            $(modal_id+' #id_levels_variable').prop('disabled', false);
        }
        else {
            $(modal_id+' #id_levels_variable').prop('disabled', true);
        }
    }

    var switchProperty = function() {
        if ($(this).is(':checked')) {
            $(modal_id+' #id_property').prop('disabled', false);
            $(modal_id+' #id_property_value').prop('disabled', false);
        }
        else {
            $(modal_id+' #id_property').prop('disabled', true);
            $(modal_id+' #id_property_value').prop('disabled', true);
        }
    }
   
    $(modal_id+' #id_collection').change( function() { loadResolutionsChain(data_form_class_name); } );
    $(modal_id+' #id_resolution').change( function() { loadScenariosChain(data_form_class_name); } );
    $(modal_id+' #id_parameteri18n').change( function() { loadTimeStepsChain(data_form_class_name); } );
    $(modal_id+' #id_time_stepi18n').change( function() { loadLvsGroupsChain(data_form_class_name); } );
    $(modal_id+' #id_levels_group').change( function() { loadLvsNamesChain(data_form_class_name); } );
    $(modal_id+' #id_use_lvsvar').change ( switchLvsVariable )
    $(modal_id+' #id_use_property').change ( switchProperty )

    // + buttons handling
    $(data_form_class_name).on('click', '.js-add-button', function() { 
        var child_modal_id = loadForm2.call(this);
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-levels-variable-form').length) {
                var form_data = mapFormData('.js-levels-variable-form');  // Get levels variable fields
                loadOptions.call(this, data_form_class_name, 'id_levels_variable',
                    'levels-variables-url', form_data['name']
                );
            };
            if ($('.js-variable-form').length) {
                var form_data = mapFormData('.js-variable-form');  // Get variable fields
                loadOptions.call(this, data_form_class_name, 'id_variable',
                    'variables-url', form_data['name']
                );
            };
            if ($('.js-unit-form').length) {
                var form_data = mapFormData('.js-unit-form');  // Get unit fields
                loadOptions.call(this, data_form_class_name, 'id_unitsi18n',
                    'units-url', form_data['name']
                );
            };
            if ($('.js-property-form').length) {
                var form_data = mapFormData('.js-property-form');  // Get property fields
                loadOptions.call(this, data_form_class_name, 'id_property',
                    'properties-url', form_data['label']
                );
            };
            if ($('.js-property-value-form').length) {
                var form_data = mapFormData('.js-property-value-form');  // Get property value fields
                loadOptions.call(this, data_form_class_name, 'id_property_value',
                    'property-values-url', form_data['label']
                );
            };
            if ($('.js-root-dir-form').length) {
                var form_data = mapFormData('.js-root-dir-form');  // Get root directory fields
                loadOptions.call(this, data_form_class_name, 'id_root_dir',
                    'root-dirs-url', form_data['name']
                );
            };
            if ($('.js-file-form').length) {
                var form_data = mapFormData('.js-file-form');  // Get file name fields
                loadOptions.call(this, data_form_class_name, 'id_file',
                    'files-url', form_data['name_pattern']
                );
            };
            $(child_modal_id).remove();
        })
    });
});