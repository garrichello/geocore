$(function() {
    var setting_form_class_name = '.js-settingfull-form';

    var emptyForm = $('<div class="form-inline combination-line">'+
                      '<div class="form-control combination-index" style="width:5%"></div> '+
                      '<select class="form-control combination-name" '+
                      'style="width: 86%"><option value="">--------</option></select></div>');

    function addCombinationSelector(string=' ') {
        var idx = $('.combination-line').length;
        var newForm = emptyForm.clone(true);
        newForm.children('div').text(idx);
        newForm.children('select').attr('id', 'id_combination_'+idx);
        newForm.children('select').attr('name', 'combination_'+idx);
        $('#id_list_of_combinations').append(newForm);
        loadOptions(setting_form_class_name, 'id_combination_'+idx, 
                    'combinations-url', string);
    };

    function setCombinationSelector(settingData) {
        for (var i=0; i<settingData.combinations.length; i++) {
            var string = settingData.combinations.filter((el) => el.index == i)[0].combination.string;
            addCombinationSelector(string);
        };
    };

    $(setting_form_class_name).on('click', '.js-add-line-button', function() {
        addCombinationSelector();
    });

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
                loadOptions.call( this, setting_form_class_name, 'id_gui_element',
                    'guielements-url', form_data['string']
                );
            };
            $(child_modal_id).remove();
        })
    });

    if ($(setting_form_class_name).attr('method') == 'PUT') {
        $.ajax({
            type: "get",
            url: $(setting_form_class_name).attr('action'),
            headers: {
                'ACTION': 'json'
            },
            dataType: "json",
            success: function (data) {
                setCombinationSelector(data.data);
            }
        });
    } else {
        addCombinationSelector();
    };
});
