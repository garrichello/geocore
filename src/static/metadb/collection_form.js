$(function() {
    var collection_form_class_name = '.'+JSON.parse($('#collection-form-class-name')[0].textContent);

    var loadOrganizations = function(form_name, organization_name='') {
        var form = $(form_name);
        var modal_id = '#'+getModalName(form.attr('action')); // Collection modal!

        if (organization_name.length) {
            $.ajax( {
                url: form.attr('organizations-url'),
                type: 'get',
                success: function (data) {
                    $(modal_id+' #id_organizationi18n').html(data);  // Get organizations names
                    $(modal_id+` #id_organizationi18n option:contains("${organization_name}")`).attr(
                        'selected', true);  // Select new organization in the select
                    if ($(modal_id+' #id_organizationi18n option').length == 2) {
                        $(modal_id+' #id_organizationi18n').prop("selectedIndex", 1);
                    }
                }
            } );
        }
    };

    // Submit form
    $('body').on('submit', '.js-collection-create-form', function(e) {
        saveForm2.call(this, e); return false; 
    });

    // Create organization modal
    $(collection_form_class_name).on('click', '.js-add-button', function() { 
        var modal_id = loadForm2.call(this);
        $(modal_id).on('hidden.bs.modal', function() {
            var form_data = mapFormData('.js-organization-create-form');  // Get fields of the form as a map
            if ('name' in form_data) {
                if (form_data['name'].length) {
                    loadOrganizations.call(this, collection_form_class_name, form_data['name']);
                }
                $(modal_id).remove();
            }
        });
    });
});