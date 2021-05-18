$(function() {
    var edge_form_class_name = '.js-edge-form';

    // + buttons handling
    $(edge_form_class_name).on('click', '.js-add-button', function() {
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-conveyor-form').length) {
                var form_data = mapFormData('.js-conveyor-form');  // Get conveyor fields
                loadOptions.call( this, edge_form_class_name, 'id_conveyor',
                    'conveyors-url', form_data['label']
                );
            };
            if ($('.js-datavariable-form').length) {
                var form_data = mapFormData('.js-datavariable-form');  // Get data variable fields
                loadOptions.call(this, edge_form_class_name, 'id_data_variable',
                    'datavariables-url', form_data['label']
                );
            };
            $(child_modal_id).remove();
        })
    });
});
