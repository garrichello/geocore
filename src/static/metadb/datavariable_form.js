$(function() {
    var datavariable_form_class_name = '.js-datavariable-form';

    // + buttons handling
    $(datavariable_form_class_name).on('click', '.js-add-button', function() {
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-unit-form').length) {
                var form_data = mapFormData('.js-unit-form');  // Get unit fields
                loadOptions.call(this, datavariable_form_class_name, 'id_units',
                    'units-url', form_data['unitsi18n.name']
                );
            };
            $(child_modal_id).remove();
        })
    });
});
