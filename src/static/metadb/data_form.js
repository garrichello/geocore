$(function () {
    var data_form_class_name = '.js-data-create-form';
    var modal_id = '#'+getModalName($(data_form_class_name).attr('action'));

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
            url: form.attr('parameter-lvsnames-url'),  // given a parameter load lvsnames
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

    var loadOptions = function(form_name, select_name, data_url, option_name='') {
        var form = $(form_name);
        var modal_id = '#'+getModalName(form.attr('action'));

        if (option_name.length) {
            $.ajax( {
                url: form.attr(data_url),
                type: 'get',
                success: function (data) {
                    $(`${modal_id} #${select_name}`).html(data);
                    $(`${modal_id} #${select_name} option`).filter(function() {
                        return $(this).text() === option_name;
                    }).attr('selected', true);  // Select given entry in the select
                    if ($(`${modal_id} #${select_name} option`).length == 2) {
                        $(`${modal_id} #${select_name}`).prop("selectedIndex", 1);
                    }
                }
            } );
        }
    };
    
    $(modal_id+' #id_collection').change( function() { loadResolutionsChain(data_form_class_name); } );
    $(modal_id+' #id_resolution').change( function() { loadScenariosChain(data_form_class_name); } );
    $(modal_id+' #id_parameteri18n').change( function() { loadTimeStepsChain(data_form_class_name); } );
    $(modal_id+' #id_time_stepi18n').change( function() { loadLvsGroupsChain(data_form_class_name); } );
    $(modal_id+' #id_levels_group').change( function() { loadLvsNamesChain(data_form_class_name); } );
    $(modal_id+' #id_use_lvsvar').change ( switchLvsVariable )
    $(modal_id+' #id_use_property').change ( switchProperty )

    // + buttons handling
    $(data_form_class_name).on('click', '.js-add-button', function() { 
        var modal_id = loadForm2.call(this);
        $(modal_id).on('hidden.bs.modal', function() {
            if ($('.js-levels-variable-create-form').length) {
                var form_data = mapFormData('.js-levels-variable-create-form');  // Get levels variable fields
                loadOptions.call(this, data_form_class_name, 'id_levels_variable',
                    'levels-variables-url', form_data['name']
                );
            };
            if ($('.js-variable-create-form').length) {
                var form_data = mapFormData('.js-variable-create-form');  // Get variable fields
                loadOptions.call(this, data_form_class_name, 'id_variable',
                    'variables-url', form_data['name']
                );
            };
            if ($('.js-unit-create-form').length) {
                var form_data = mapFormData('.js-unit-create-form');  // Get unit fields
                loadOptions.call(this, data_form_class_name, 'id_unitsi18n',
                    'units-url', form_data['name']
                );
            };
            if ($('.js-property-create-form').length) {
                var form_data = mapFormData('.js-property-create-form');  // Get property fields
                loadOptions.call(this, data_form_class_name, 'id_property',
                    'properties-url', form_data['label']
                );
            };
            if ($('.js-property-value-create-form').length) {
                var form_data = mapFormData('.js-property-value-create-form');  // Get property value fields
                loadOptions.call(this, data_form_class_name, 'id_property_value',
                    'property-values-url', form_data['label']
                );
            };
            if ($('.js-root-dir-create-form').length) {
                var form_data = mapFormData('.js-root-dir-create-form');  // Get root directory fields
                loadOptions.call(this, data_form_class_name, 'id_root_dir',
                    'root-dirs-url', form_data['name']
                );
            };
            if ($('.js-file-create-form').length) {
                var form_data = mapFormData('.js-file-create-form');  // Get file name fields
                loadOptions.call(this, data_form_class_name, 'id_file',
                    'files-url', form_data['name_pattern']
                );
            };
            $(modal_id).remove();
        })
    });
});