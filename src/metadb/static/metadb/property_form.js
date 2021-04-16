$(function() {
    var simple_form_class_name = '.js-property-form';

    // Create property modal
    $(simple_form_class_name).on('click', '.js-add-button', function() { 
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            var form_data = mapFormData('.js-gui-element-form');  // Get fields of the form as a map
            if ('name' in form_data) {
                if (form_data['name'].length) {
                    loadOptions.call(this, simple_form_class_name, 'id_gui_element', 
                        'gui-element-url', form_data['name']
                    );
                }
                $(child_modal_id).remove();
            }
        });
    });
});