$(function() {
    var vertex_form_class_name = '.js-vertex-form';

    // + buttons handling
    $(vertex_form_class_name).on('click', '.js-add-button', function() {
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-computingmodule-form').length) {
                var form_data = mapFormData('.js-computingmodule-form');  // Get computing module fields
                loadOptions.call( this, vertex_form_class_name, 'id_computing_module',
                    'computingmodules-url', form_data['name']
                );
                console.log(form_data['name']);
            };
            if ($('.js-combination-form').length) {
                var form_data = mapFormData('.js-combination-form');  // Get combination fields
                loadOptions.call(this, vertex_form_class_name, 'id_condition_combination',
                    'combinations-url', form_data['option']
                );
            };
            $(child_modal_id).remove();
        })
    });
});
