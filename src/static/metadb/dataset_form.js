$(function() {
    var dataset_form_class_name = '.js-dataset-form';

    // + buttons handling
    $(dataset_form_class_name).on('click', '.js-add-button', function() {
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-collection-form').length) {
                var form_data = mapFormData('.js-collection-form');  // Get collection fields
                loadOptions.call( this, dataset_form_class_name, 'id_collection_label',
                    'collections-url', form_data['label']
                );
            };
            if ($('.js-resolution-form').length) {
                var form_data = mapFormData('.js-resolution-form');  // Get resolution fields
                loadOptions.call(this, dataset_form_class_name, 'id_resolution_name',
                    'resolutions-url', form_data['name']
                );
            };
            if ($('.js-scenario-form').length) {
                var form_data = mapFormData('.js-scenario-form');  // Get scenario fields
                loadOptions.call(this, dataset_form_class_name, 'id_scenario_name',
                    'scenarios-url', form_data['name']
                );
            };
            if ($('.js-datakind-form').length) {
                var form_data = mapFormData('.js-datakind-form');  // Get datakind fields
                loadOptions.call(this, dataset_form_class_name, 'id_data_kind_name',
                    'datakinds-url', form_data['name']
                );
            };
            if ($('.js-filetype-form').length) {
                var form_data = mapFormData('.js-filetype-form');  // Get filetype fields
                loadOptions.call(this, dataset_form_class_name, 'id_file_type_name',
                    'filetypes-url', form_data['name']
                );
            };
            $(child_modal_id).remove();
        })
    });
});
