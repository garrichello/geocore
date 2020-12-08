$(function() {
    var levels_group_form_class_name = '.js-levels-group-form';

    // + buttons handling
    $(levels_group_form_class_name).on('click', '.js-add-button', function() {
        var modal_id = loadForm2.call(this);
        $(modal_id).on('hidden.bs.modal', function() {
            if ($('.js-unit-form').length) {
                var form_data = mapFormData('.js-unit-form');  // Get units fields
                loadOptions.call( this, levels_group_form_class_name, 'id_unitsi18n',
                    'units-url', form_data['name']
                );
            };
            $(modal_id).remove();
        })
    });
});
