$(function() {
    var collection_form_class_name = '.js-collection-form';

    // Create organization modal
    $(collection_form_class_name).on('click', '.js-add-button', function() { 
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            var form_data = mapFormData('.js-organization-form');  // Get fields of the form as a map
            field_name = 'organizationi18n.name';
            if (field_name in form_data) {
                if (form_data[field_name].length) {                  
                    loadOptions.call(this, collection_form_class_name, 'id_organization',
                    'organizations-url', form_data[field_name]
                );                    
                }
                $(child_modal_id).remove();
            }
        });
    });
});