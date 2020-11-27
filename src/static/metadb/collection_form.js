var form_class_name = '.'+JSON.parse($('#collection-form-class-name')[0].textContent);

var loadOrganizations = function(form_name, organization_name='') {
    var form = $(form_name);
    var modal_id = '#'+getModalName(form.attr('action')); // Collection modal!

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
};

var organization_form_class = '.js-organization-create-form';
$('body').on('submit', organization_form_class, function(e) {
    saveForm2.call(this, e);  // Save new organization
    form_data = mapFormData(organization_form_class);  // Get fields of the form as a map
    loadOrganizations.call(this, form_class_name, form_data['name']);
    return false; 
});