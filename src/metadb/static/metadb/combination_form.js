$(function() {
    var combination_form_class_name = '.js-combination-form';
    var modal_id = '#'+getModalName();
    var optionLabel = '';
    var optionValue = '';
    var condition = '';

    function setString() {
        var stringVal = '-';
        if (optionLabel != '-') {
            stringVal = `${optionLabel}=${optionValue}`;
        };
        if (condition != '') {
            stringVal = stringVal + ` [if ${condition}]`;
        }
        $(combination_form_class_name+' #id_string').attr('value', stringVal);
    }

    $(modal_id+' #id_option').on('change', (e) => {
        optionLabel = $(e.target).find('option:selected').text();
        setString();
    });

    $(modal_id+' #id_option_value').on('change', (e) => {
        optionValue = $(e.target).find('option:selected').text();
        setString();
    });

    $(modal_id+' #id_condition').on('change', (e) => {
        condition = $(e.target).find('option:selected').text();
        setString();
    });


    // + buttons handling
    $(combination_form_class_name).on('click', '.js-add-button', function() {
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-option-form').length) {
                var form_data = mapFormData('.js-option-form');  // Get option fields
                loadOptions.call( this, combination_form_class_name, 'id_option',
                    'options-url', form_data['label']
                );
            };
            if ($('.js-optionvalue-form').length) {
                var form_data = mapFormData('.js-optionvalue-form');  // Get option value fields
                loadOptions.call(this, combination_form_class_name, 'id_option_value',
                    'optionvalues-url', form_data['label']
                );
            };
            $(child_modal_id).remove();
        })
    });
});