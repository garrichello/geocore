var loadScenarios = function(form_name) {
    var form = $(form_name);
    var collectionId = $('#modal-data #id_collection').val();
    var resolutionId = $('#modal-data #id_resolution').val();

    $.ajax( {
        url: form.attr('dataset-scenario-url'),
        type: 'get',
        data: {
            'collectionId': collectionId,
            'resolutionId': resolutionId,
        },
        success: function (data) {
            $('#modal-data #id_scenario').html(data);
            if ($('#modal-data #id_scenario option').length == 2) {
                $('#modal-data #id_scenario').prop("selectedIndex", 1);
            }
        }
    } );
};

var loadResolutions = function(form_name) {
    var form = $(form_name);
    var collectionId = $('#modal-data #id_collection').val();

    $.ajax( {
        url: form.attr('dataset-resolutions-url'),
        type: 'get',
        data: {
            'collectionId': collectionId,
        },
        success: function (data) {
            $('#modal-data #id_resolution').html(data);
            if ($('#modal-data #id_resolution option').length == 2) {
                $('#modal-data #id_resolution').prop("selectedIndex", 1);
            }
            $('#modal-data #id_resolution').trigger('change');
        }
    } );
};

var loadLvsGroups = function(form_name) {
    var form = $(form_name);
    var parameteri18nId = $('#modal-data #id_parameteri18n').val();
    var timestepi18nId = $('#modal-data #id_time_stepi18n').val();

    $.ajax( {
        url: form.attr('parameter-lvsgroups-url'),
        type: 'get',
        data: {
            'parameteri18nId': parameteri18nId,
            'timestepi18nId': timestepi18nId,
        },
        success: function (data) {
            $('#modal-data #id_levels_group').html(data);
            if ($('#modal-data #id_levels_group option').length == 2) {
                $('#modal-data #id_levels_group').prop("selectedIndex", 1);
            }
            $('#modal-data #id_levels_group').trigger('change');
        }
    } );
};

var loadTimeSteps = function(form_name) {
    var form = $(form_name);
    var parameteri18nId = $('#modal-data #id_parameteri18n').val();

    $.ajax( {
        url: form.attr('parameter-timesteps-url'),
        type: 'get',
        data: {
            'parameteri18nId': parameteri18nId,
        },
        success: function (data) {
            $('#modal-data #id_time_stepi18n').html(data);
            if ($('#modal-data #id_time_stepi18n option').length == 2) {
                $('#modal-data #id_time_stepi18n').prop("selectedIndex", 1);
            }
            $('#modal-data #id_time_stepi18n').trigger('change');
        }
    } );
};

var loadLvsNames = function(form_name) {
    var form = $(form_name);
    var lvsgroupId = $('#modal-data #id_levels_group').val();

    $.ajax( { 
        url: form.attr('parameter-lvsnames-url'),
        type: 'get',
        data: {
            'lvsgroupId': lvsgroupId,
        },
        success: function (data) {
            $('#modal-data #id_levels_namesi18n').val(data);
        }
    } );
};

var switchLvsVariable = function() {
    if ($(this).is(':checked')) {
        $('#modal-data #id_levels_variable').prop('disabled', false);
    }
    else {
        $('#modal-data #id_levels_variable').prop('disabled', true);
    }
}

var switchProperty = function() {
    if ($(this).is(':checked')) {
        $('#modal-data #id_property').prop('disabled', false);
        $('#modal-data #id_property_value').prop('disabled', false);
    }
    else {
        $('#modal-data #id_property').prop('disabled', true);
        $('#modal-data #id_property_value').prop('disabled', true);
    }
}

var form_class_name = '.'+JSON.parse($('#form-class-name')[0].textContent);
$('#modal-data #id_collection').change( function() { loadResolutions(form_class_name); } );
$('#modal-data #id_resolution').change( function() { loadScenarios(form_class_name); } );
$('#modal-data #id_parameteri18n').change( function() { loadTimeSteps(form_class_name); } );
$('#modal-data #id_time_stepi18n').change( function() { loadLvsGroups(form_class_name); } );
$('#modal-data #id_levels_group').change( function() { loadLvsNames(form_class_name); } );
$('#modal-data #id_use_lvsvar').change ( switchLvsVariable )
$('#modal-data #id_use_property').change ( switchProperty )
