$(function() {
    var simple_form_class_name = '.js-procarggroup-form';

    // Create property modal
    $(simple_form_class_name).on('click', '.js-add-button', function() { 
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-procarggroup-form').length) {
                var form_data = mapFormData('.js-procarggroup-form');  // Get fields of the form as a map
                loadOptions.call(this, simple_form_class_name, 'id_arguments_group', 
                    'argumentsgroups-url', form_data['name']
                );
            };
            if ($('.js-processor-form').length) {
                var form_data = mapFormData('.js-processor-form');  // Get fields of the form as a map
                loadOptions.call(this, simple_form_class_name, 'id_processor', 
                    'processors-url', form_data['processori18n.name']
                );
            };
            if ($('.js-settingfull-form').length) {
                var form_data = mapFormData('.js-settingfull-form');  // Get fields of the form as a map
                loadOptions.call(this, simple_form_class_name, 'id_override_setting', 
                    'settings-url', form_data['label']
                );
            };
            $(child_modal_id).remove();
        });
    });
});