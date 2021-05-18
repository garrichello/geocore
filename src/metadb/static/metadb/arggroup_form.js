$(function() {
    var arggroup_form_class_name = '.js-arggroup-form';

    // Create organization modal
    $(arggroup_form_class_name).on('click', '.js-add-button', function() { 
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-argtype-form').length) {
                var form_data = mapFormData('.js-argtype-form');  // Get argument type fields
                loadOptions.call( this, arggroup_form_class_name, 'id_argument_type',
                    'argtypes-url', form_data['label']
                );
            };
            $(child_modal_id).remove();
        });
    });

    $('#id_argument_type').trigger('change');
});