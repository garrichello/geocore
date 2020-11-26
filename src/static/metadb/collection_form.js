var form_class_name = '.'+JSON.parse($('#form-class-name')[0].textContent);

var loadOrganizations = function(form_name) {
    var form = $(form_name);

    $.ajax( {
        url: form.attr('organizations-url'),
        type: 'get',
        success: function (data) {
            $('#modal-collection #id_organizationi18n').html(data);
            if ($('#modal-collection #id_organizationi18n option').length == 2) {
                $('#modal-collection #id_organizationi18n').prop("selectedIndex", 1);
            }
        }
    } );
};

$('#modal-over').on('submit', '.js-organization-create-form', function(e) {
    saveForm.call(this, e, '#modal-over');
    loadOrganizations.call(this, form_class_name);
    return false; 
});