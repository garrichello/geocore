$(function () {
    var data_form_class_name = '.'+JSON.parse($('#data-form-class-name')[0].textContent);
    var modal_id = '#'+getModalName($(data_form_class_name).attr('action'));

    var loadScenariosChain = function(form_name) {
        var form = $(form_name);
        var collectionId = $(modal_id+' #id_collection').val();
        var resolutionId = $(modal_id+' #id_resolution').val();
    
        $.ajax( {
            url: form.attr('dataset-scenario-url'),
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
            url: form.attr('dataset-resolutions-url'),
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
            url: form.attr('parameter-lvsgroups-url'),
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
            url: form.attr('parameter-timesteps-url'),
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
            url: form.attr('parameter-lvsnames-url'),
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

    // Submit form
    $('body').on('submit', '.js-data-create-form', function(e) {
        saveForm2.call(this, e); return false;
    });
    
    $(modal_id+' #id_collection').change( function() { loadResolutionsChain(data_form_class_name); } );
    $(modal_id+' #id_resolution').change( function() { loadScenariosChain(data_form_class_name); } );
    $(modal_id+' #id_parameteri18n').change( function() { loadTimeStepsChain(data_form_class_name); } );
    $(modal_id+' #id_time_stepi18n').change( function() { loadLvsGroupsChain(data_form_class_name); } );
    $(modal_id+' #id_levels_group').change( function() { loadLvsNamesChain(data_form_class_name); } );
    $(modal_id+' #id_use_lvsvar').change ( switchLvsVariable )
    $(modal_id+' #id_use_property').change ( switchProperty )


});