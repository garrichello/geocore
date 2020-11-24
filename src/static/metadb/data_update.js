var loadScenarios = function() {
    var form = $('.js-data-update-form');
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

var loadResolutions = function() {
    var form = $('.js-data-update-form');
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

var loadLvsGroups = function() {
    var form = $('.js-data-update-form');
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

var loadTimeSteps = function() {
    var form = $('.js-data-update-form');
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
            $('#modal-data #id_levels_group').trigger('change');
        }
    } );
};

var loadLvsNames = function() {
    var form = $('.js-data-update-form');
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

$('#modal-data #id_collection').change( loadResolutions );
$('#modal-data #id_resolution').change( loadScenarios );
$('#modal-data #id_parameteri18n').change( loadTimeSteps );
$('#modal-data #id_time_stepi18n').change( loadLvsGroups );
$('#modal-data #id_levels_group').change( loadLvsNames );
