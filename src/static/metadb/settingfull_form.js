$(function() {
    var setting_form_class_name = '.js-settingfull-form';

    // + buttons handling
    $(setting_form_class_name).on('click', '.js-add-button', function() {
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-gui-element-form').length) {
                var form_data = mapFormData('.js-gui-element-form');  // Get gui element fields
                loadOptions.call( this, setting_form_class_name, 'id_gui_element',
                    'guielements-url', form_data['name']
                );
            };
            if ($('.js-combination-form').length) {
                var form_data = mapFormData('.js-combination-form');  // Get combination fields
                console.log(form_data);
                loadOptions.call( this, setting_form_class_name, 'id_gui_element',
                    'guielements-url', form_data['name']
                );
            };
            $(child_modal_id).remove();
        })
    });
});
