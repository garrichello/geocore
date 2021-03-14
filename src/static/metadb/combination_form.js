$(function() {
    var combination_form_class_name = '.js-combination-form';

    // + buttons handling
    $(combination_form_class_name).on('click', '.js-add-button', function() {
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-option-form').length) {
                var form_data = mapFormData('.js-option-form');  // Get option fields
                loadOptions.call( this, combination_form_class_name, 'id_option',
                    'options-url', form_data['label']
                );
            };
            if ($('.js-optionvalue-form').length) {
                var form_data = mapFormData('.js-optionvalue-form');  // Get option value fields
                loadOptions.call(this, combination_form_class_name, 'id_option_value',
                    'optionvalues-url', form_data['label']
                );
            };
            $(child_modal_id).remove();
        })
    });
});