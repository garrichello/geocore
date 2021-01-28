$(function() {
    var loadOptions = function(form_name, select_name, data_url, option_name='') {
        var form = $(form_name);
        var modal_id = '#'+getModalName('parent');

        if (option_name.length) {
            $.ajax( {
                url: form.attr(data_url),
                type: 'get',
                success: function (data) {
                    $(`${modal_id} #${select_name}`).html(data);
                    $(`${modal_id} #${select_name} option`).filter(function() {
                        return $(this).text() === option_name;
                    }).attr('selected', true);  // Select given entry in the select
                    if ($(`${modal_id} #${select_name} option`).length == 2) {
                        $(`${modal_id} #${select_name}`).prop("selectedIndex", 1);
                    }
                }
            } );
        }
    };

    // Create organization modal
    var simple_form_class_name = '.js-property-form';
    $(simple_form_class_name).on('click', '.js-add-button', function() { 
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            var form_data = mapFormData('.js-gui-element-form');  // Get fields of the form as a map
            if ('name' in form_data) {
                if (form_data['name'].length) {
                    loadOptions.call(this, simple_form_class_name, 'id_gui_element', 
                        'gui-element-url', form_data['name']
                    );
                }
                $(child_modal_id).remove();
            }
        });
    });
});