$(function() {
    var levels_group_form_class_name = '.js-levels-group-form';
    var modal_id = '#'+getModalName();

    var loadLvsNames = function() {
        var form = $(levels_group_form_class_name);
    
        $.ajax( { 
            url: form.attr('levels-url'),  // load lvsnames
            type: 'get',
            success: function (data) {
                $(modal_id+' #available_levels_list').html(data);
            }
        } );
    };

    loadLvsNames();

    var sortLevels = function(listId) {
        var mylist = $(listId);
        var listitems = mylist.children('a').get();
        listitems.sort(function(a, b) {
           return $(a).text().toUpperCase().localeCompare($(b).text().toUpperCase());
        })
        $.each(listitems, function(idx, itm) { mylist.append(itm); });        
    }

    var getLi = function(action, name) {
        return $(`<a href="#" class="list-group-item js-${action}-level-button">${name}</a>`);
    }

    // Store current list of selected levels in the hidden input
    var storeList = function() {
        var list = $.map($(modal_id+' #selected_levels_list a'), function(n, i) {
            return ($(n).text());
        });
        $(modal_id+' #id_selected_levels').val(JSON.stringify(list));
    }

    var addLevel = function(obj) {
        var name = $(obj).text();
        $(modal_id+' #selected_levels_list').append(getLi('remove', name));
        $(obj).remove();
        storeList();
    }

    var removeLevel = function(obj) {
        var name = $(obj).text();
        $(modal_id+' #available_levels_list').append($(getLi('add', name)));
        $(obj).remove();
        storeList();
    }

    // Add one level
    $(levels_group_form_class_name).on('click', '.js-add-level-button', function() {
        addLevel(this);
        sortLevels('#selected_levels_list');
    });

    // Add all levels
    $(levels_group_form_class_name).on('click', '#js-add-all-levels-button', function() {
        $.each($(modal_id+' #available_levels_list a'), function(index, value) {
            addLevel(value);
        });
        sortLevels('#selected_levels_list');
    });

    // Remove one level
    $(levels_group_form_class_name).on('click', '.js-remove-level-button', function() {
        removeLevel(this);
        sortLevels('#available_levels_list');
    });

    // Remove all levels
    $(levels_group_form_class_name).on('click', '#js-remove-all-levels-button', function() {
        $.each($(modal_id+' #selected_levels_list a'), function(index, value) {
            removeLevel(value);
        });
        sortLevels('#available_levels_list');
    });

    // + buttons handling
    $(levels_group_form_class_name).on('click', '.js-add-button', function() {
        var child_modal_id = loadForm2.call(this, 'create');
        var dismissed = false;
        $(child_modal_id).on('click.dismiss.bs.modal', '[data-dismiss="modal"]', function() {
            dismissed = true;
        })
        $(child_modal_id).on('hidden.bs.modal', function() {
            if ($('.js-unit-form').length) {
                var form_data = mapFormData('.js-unit-form');  // Get unit fields
                loadOptions.call(this, levels_group_form_class_name, 'id_unitsi18n',
                    'units-url', form_data['name']
                );
            };
            if ($('.js-level-form').length && !dismissed) {
                var form_data = mapFormData('.js-level-form');  // Get level fields
                $(modal_id+' #available_levels_list').append(getLi('add', form_data['label']));
                sortLevels('#available_levels_list');
            };
            $(child_modal_id).remove();
        })
    });
});
