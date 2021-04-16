$(function() {
    var arggroupfull_form_class_name = '.js-arggroupfull-form';

    $('#id_argument_type').on('change', (e) => {
        var argType = $(e.target).find('option:selected').text();
        if (argType == 'data') {
            $('#id_processor').attr('disabled', true);
            $('#id_specific_parameter').attr('disabled', false);
        } else if (argType == 'processor') {
            $('#id_processor').attr('disabled', false);
            $('#id_specific_parameter').attr('disabled', true);
        }
    })

    // Create organization modal
    $(arggroupfull_form_class_name).on('click', '.js-add-button', function() { 
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-argtype-form').length) {
                var form_data = mapFormData('.js-argtype-form');  // Get argument type fields
                loadOptions.call( this, arggroupfull_form_class_name, 'id_argument_type',
                    'argtypes-url', form_data['label']
                );
            };
            if ($('.js-processor-form').length) {
                var form_data = mapFormData('.js-processor-form');  // Get processor fields
                loadOptions.call(this, arggroupfull_form_class_name, 'id_processor',
                    'processors-url', form_data['processori18n.name']
                );
            };
            if ($('.js-specpar-form').length) {
                var form_data = mapFormData('.js-specpar-form');  // Get specific parameter fields
                loadOptions.call(this, arggroupfull_form_class_name, 'id_specific_parameter',
                    'specificparameters-url', form_data['string']
                );
            };
            $(child_modal_id).remove();
        });
    });

    $('#id_argument_type').trigger('change');
});