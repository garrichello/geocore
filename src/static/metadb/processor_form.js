$(function() {
    var processor_form_class_name = '.js-processor-form';
    var fullargumentsgroup_url = $(processor_form_class_name).attr('fullargumentsgroups-url')+'-1/';
    var placeholderText = $('#id_list_of_arguments').attr('placeholder');

    var emptyForm = $('<div class="form-inline arguments-line">'+
                      '<div class="form-control arguments-position" style="width:5%"></div> '+
                      '<select class="form-control arguments-group" name="arguments_group" '+
                      'style="width: 86%"><option value="" selected>--------</option></select></div>');
    var addButton = $('<button type="button" class="btn btn-primary js-add-button" '+
                      `data-url="${fullargumentsgroup_url}"> `+
                      '<span class="glyphicon glyphicon-plus"></span></button>');
    var noArgGroups = $(`<div class="arguments-line">${placeholderText}</div>`);

    function addArgumentsGroupsSelector(addAddButton=false) {
        var idx = $('.arguments-line').length+1;
        var newForm = emptyForm.clone(true);
        newForm.children('div').text(idx);
        newForm.children('select').attr('id', 'id_arguments_group_'+idx);
        if (addAddButton) {
            newForm.append(' '); // Small separator
            newForm.append(addButton);
        }
        $('#id_list_of_arguments').append(newForm);
        loadOptions(processor_form_class_name, 'id_arguments_group_'+idx, 
                    'argumentsgroups-url', ' ', parent=true);
    };

    function setArgumentsGroupsSelectors(count=0) {
        var argSelectors = $('.arguments-line');
        argSelectors.remove();
        for (var i=0; i<count; i++) {
            addArgumentsGroupsSelector(addAddButton=(i==0));
        }
    }

    $(processor_form_class_name+' #id_conveyor').on('change', function(e) {
        var conveyor_id = this.value;
        if (conveyor_id) {
            var url = $(processor_form_class_name).attr('fullconveyors-url')+conveyor_id;
            $.ajax({
                type: "get",
                headers: {
                    'ACTION': 'json',
                },
                url: url,
                dataType: "json",
                success: function (data) {
                    var numberOfInputs = 0;
                    data.data.edges.forEach(edge => {
                        if (edge.from_vertex.computing_module.name == 'START' && edge.from_output > 0) {
                            numberOfInputs += 1;
                        }
                    });
                    setArgumentsGroupsSelectors(numberOfInputs);
                }
            });
        } else {
            var argSelectors = $('.arguments-line');
            argSelectors.remove();
            $('#id_list_of_arguments').append(noArgGroups);
        }
    });

    // + buttons handling
    $(processor_form_class_name).on('click', '.js-add-button', function() {
        var child_modal_id = loadForm2.call(this, 'create');
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-conveyor-form').length) {
                var form_data = mapFormData('.js-conveyor-form');  // Get conveyor fields
                loadOptions.call( this, processor_form_class_name, 'id_conveyor',
                    'conveyors-url', form_data['label']
                );
            };
            if ($('.js-datavariable-form').length) {
                var form_data = mapFormData('.js-datavariable-form');  // Get data variable fields
                loadOptions.call(this, processor_form_class_name, 'id_data_variable',
                    'datavariables-url', form_data['label']
                );
            };
            $(child_modal_id).remove();
        })
    });

    // Add some placeholder text where arguments group selectors should be
    $('#id_list_of_arguments').append(noArgGroups);

});
