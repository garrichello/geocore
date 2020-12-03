$(function() {
    var dataset_form_class_name = '.'+JSON.parse($('#dataset-form-class-name')[0].textContent);

    var loadOptions = function(form_name, select_name, data_url, option_name) {
        var form = $(form_name);
        var modal_id = '#'+getModalName(form.attr('action'));

        if (option_name.length) {
            $.ajax( {
                url: form.attr(data_url),
                type: 'get',
                success: function (data) {
                    $(`${modal_id} #${select_name}`).html(data);
                    $(`${modal_id} #${select_name} option:contains("${option_name}")`).attr(
                        'selected', true);  // Select given entry in the select
                    if ($(`${modal_id} #${select_name} option`).length == 2) {
                        $(`${modal_id} #${select_name}`).prop("selectedIndex", 1);
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
                loadOptions.call( this, dataset_form_class_name, 'id_collection', 'collections-url',
                    form_data['label']
                );
            };
            if ($('.js-resolution-create-form').length) {
                var form_data = mapFormData('.js-resolution-create-form');  // Get resolution fields
                loadOptions.call(this, dataset_form_class_name, 'id_resolution', 'resolutions-url',
                    form_data['name']
                );
            };
            if ($('.js-scenario-create-form').length) {
                var form_data = mapFormData('.js-scenario-create-form');  // Get scenario fields
                loadOptions.call(this, dataset_form_class_name, 'id_scenario', 'scenarios-url',
                    form_data['name']
                );
            };
            if ($('.js-datakind-create-form').length) {
                var form_data = mapFormData('.js-datakind-create-form');  // Get datakind fields
                loadOptions.call(this, dataset_form_class_name, 'id_data_kind', 'datakinds-url',
                    form_data['name']
                );
            };
            if ($('.js-filetype-create-form').length) {
                var form_data = mapFormData('.js-filetype-create-form');  // Get filetype fields
                loadOptions.call(this, dataset_form_class_name, 'id_file_type', 'filetypes-url',
                    form_data['name']
                );
            };
            $(modal_id).remove();
        })
    });
});
