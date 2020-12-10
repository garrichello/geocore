$(function() {
    var collection_form_class_name = '.js-collection-form';

    // Create organization modal
    $(collection_form_class_name).on('click', '.js-add-button', function() { 
        var child_modal_id = loadForm2.call(this);
        $(child_modal_id).on('hidden.bs.modal', function() {
            var form_data = mapFormData('.js-organization-form');  // Get fields of the form as a map
            if ('name' in form_data) {
                if (form_data['name'].length) {                  
                    loadOptions.call(this, collection_form_class_name, 'id_organizationi18n',
                    'organizations-url', form_data['name']
                );                    
                }
                $(child_modal_id).remove();
            }
        });
    });
});