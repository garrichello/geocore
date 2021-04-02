$(function() {
    var simple_form_class_name = '.js-optionsoverride-form';

    // Create property modal
    $(simple_form_class_name).on('click', '.js-add-button', function() { 
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-arggroup-form').length) {
                var form_data = mapFormData('.js-arggroup-form');  // Get fields of the form as a map
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
            if ($('.js-combination-form').length) {
                var form_data = mapFormData('.js-combination-form');  // Get fields of the form as a map
                loadOptions.call(this, simple_form_class_name, 'id_combination', 
                    'combinations-url', form_data['string']
                );
            };
            $(child_modal_id).remove();
        });
    });
});