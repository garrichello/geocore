$(function() {
    var arggroupfull_form_class_name = '.js-dataarggroup-form';

    // Create data argument group modal
    $(arggroupfull_form_class_name).on('click', '.js-add-button', function() { 
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-specpar-form').length) {
                var form_data = mapFormData('.js-specpar-form');  // Get specific parameter fields
                loadOptions.call(this, arggroupfull_form_class_name, 'id_specific_parameter',
                    'specificparameters-url', form_data['string']
                );
            };
            $(child_modal_id).remove();
        });
    });
});