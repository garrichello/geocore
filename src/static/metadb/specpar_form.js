$(function() {
    var specpar_form_class_name = '.js-specpar-form';
    var modal_id = '#'+getModalName('parent');

    var loadLvsNamesChain = function(form_name) {
        var form = $(form_name);
        var lvsgroupId = $(modal_id+' #id_levels_group').val();
    
        $.ajax( { 
            url: form.attr('lvsgroup-lvsnames-url'),  // given a parameter load lvsnames
            type: 'get',
            data: {
                'lvsgroupId': lvsgroupId,
            },
            success: function (data) {
                $(modal_id+' #id_levels_namesi18n').val(data);
            }
        } );
    };

    $(modal_id+' #id_levels_group').change( function() { loadLvsNamesChain(specpar_form_class_name); } );

    // + buttons handling
    $(specpar_form_class_name).on('click', '.js-add-button', function() {
        var modal_id = loadForm2.call(this);
        $(modal_id).on('hidden.bs.modal', function() {
            if ($('.js-parameter-form').length) {
                var form_data = mapFormData('.js-parameter-form');  // Get parameter fields
                loadOptions.call( this, specpar_form_class_name, 'id_parameteri18n', 'parameter-url',
                    form_data['name']
                );
            };
            if ($('.js-timestep-form').length) {
                var form_data = mapFormData('.js-timestep-form');  // Get time step fields
                loadOptions.call(this, specpar_form_class_name, 'id_time_stepi18n', 'time-step-url',
                    form_data['name']
                );
            };
            if ($('.js-lvsgroup-form').length) {
                var form_data = mapFormData('.js-lvsgroup-form');  // Get levels group fields
                loadOptions.call(this, specpar_form_class_name, 'id_levels_group', 'levels-group-url',
                    form_data['name']
                );
            };
            $(modal_id).remove();
        })
    });
});
