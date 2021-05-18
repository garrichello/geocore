$(function() {
    var specpar_form_class_name = '.js-specpar-form';
    var modal_id = '#'+getModalName();
    var parameterName = '';
    var timeStepName = '';
    var levelsGroupName = '';

/*    var loadLvsNamesChain = function(form_name) {
        var form = $(form_name);
        var lvsgroupId = $(modal_id+' #id_lvs_group').val();

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
*/
    function setString() {
        $(specpar_form_class_name+' #id_string').attr('value', `${parameterName} @ ${levelsGroupName} / ${timeStepName}`);
    }

//    $(modal_id+' #id_lvs_group').change( function() { loadLvsNamesChain(specpar_form_class_name); } );

    $(modal_id+' #id_parameter').on('change', (e) => {
        parameterName = $(e.target).find('option:selected').text();
        setString();
    });

    $(modal_id+' #id_time_step').on('change', (e) => {
        timeStepName = $(e.target).find('option:selected').text();
        setString();
    });

    $(modal_id+' #id_levels_group').on('change', (e) => {
        levelsGroupName = $(e.target).find('option:selected').text();
        setString();
    });

    // + buttons handling
    $(specpar_form_class_name).on('click', '.js-add-button', function() {
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-parameter-form').length) {
                var form_data = mapFormData('.js-parameter-form');  // Get parameter fields
                loadOptions.call( this, specpar_form_class_name, 'id_parameter', 'parameter-url',
                    form_data['parameteri18n.name']
                );
            };
            if ($('.js-timestep-form').length) {
                var form_data = mapFormData('.js-timestep-form');  // Get time step fields
                loadOptions.call(this, specpar_form_class_name, 'id_time_step', 'time-step-url',
                    form_data['timestepi18n.name']
                );
            };
            if ($('.js-levels-group-form').length) {
                var form_data = mapFormData('.js-levels-group-form');  // Get levels group fields
                loadOptions.call(this, specpar_form_class_name, 'id_levels_group', 'levels-group-url',
                    form_data['description']
                );
                $(modal_id+' #id_lvs_group').trigger('change');
            };
            $(child_modal_id).remove();
        })
    });
});
