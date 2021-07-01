$(function() {

    var addModal = function(modal_name, dialog_id) {
        if (!$('#'+modal_name).length) {
            var modal = $('<div class="modal fade" tabindex="-1" role="dialog">');
            modal.attr('id', modal_name);
            var modal_dialog = $(`<div class="modal-dialog" id="${dialog_id}">`);
            modal_dialog.appendTo(modal);
            var modal_content = $('<div class="modal-content"></div>');
            modal_content.appendTo(modal_dialog);
            $('#modal-stables').before( modal );  // In main_view.html

            // To provide a correct z-ordering of nested modals
            $(modal).on('show.bs.modal', function(event) {
                var idx = $('.modal:visible').length;
                $(this).css('z-index', 1040 + (10 * idx));
            });
            $(modal).on('shown.bs.modal', function(event) {
                var idx = ($('.modal:visible').length) -1; // raise backdrop after animation.
                $('.modal-backdrop').not('.stacked').css('z-index', 1039 + (10 * idx));
                $('.modal-backdrop').not('.stacked').addClass('stacked');
            });
            $(modal).on('hidden.bs.modal', function() {
                $('.modal:visible').length && $(document.body).addClass('modal-open'); // Make modal scrollable again!
            });
        };
    };

    getModalName = function(status) {
        var idx = $('.modal:visible').length;
        if (status == 'parent') idx = idx - 1;
        idx = idx < 0 ? 0 : idx;  // Negative numbers are not allowed
        return 'modal-dynamic-'+idx;
    };

    loadForm2 = function (action=None, dialog_id='id_modal_dialog') {
        var btn = $(this);
        var modal_name = getModalName();
        addModal(modal_name, dialog_id);
        var modal_id = '#'+modal_name;
        $.ajax({
            type: "get",
            headers: {
                'ACTION': action,
            },
            url: btn.attr("data-url"),
            dataType: 'json',
            success: function(data) {
                $(modal_id+' .modal-content').html(data.html_form);
                $(modal_id).modal('show');
            },
            error: function(xhr, errmsg, err) {
                console.error('Error occured when loading form data');
//                $(modal_name+' .modal-content').html(xhr.responseText);
//                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
        return modal_id;
    };

    saveForm2 = function(e) {
        e.stopImmediatePropagation();
        var form = $(this);
        var modal_id = '#'+getModalName('parent');
        var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        $.ajax({
            type: form.attr('method'),
            headers: {
                'X-CSRFToken': csrftoken
            },
            url: form.attr('action'),
            data: form.serialize(),
            dataType: 'json',
            success: function(data) {
                if (data.form_is_valid) {
                    $.fn.dataTable.tables( {visible: false, api: true} ).ajax.reload();
                    $(modal_id).modal('hide');
                }
                else {
                    $(modal_id+' .modal-content').html(data.html_form);
                }
            },
            error: function(xhr, errmsg, err) {
                alert('Error occured when saving form data');
//                $(modal_name+' .modal-content').html(xhr.responseText);
//                console.log(xhr.status + ": " + xhr.responseText);
            },
        });
        return false;
    };

    mapFormData = function(form_class) {
        var form_data = $(form_class).serializeArray().reduce(function(obj, item) {
            obj[item.name] = item.value;
            return obj;
        }, {});
        return form_data;
    };

    loadOptions = function(form_name, select_name, data_url, option_names=[], parent=false) {
        var form = $(form_name);
        var option_names = $.type(option_names) === 'array' ? option_names : Array(option_names);
        if (option_names.length) {
            $.ajax( {
                type: 'get',
                headers: {
                    'ACTION': 'options_list',
                },
                url: form.attr(data_url),
                success: function (data) {
                    $(`${form_name} #${select_name}`).html(data);
                    $(`${form_name} #${select_name} option`).filter(function() {
                        return $.inArray( $(this).text(), option_names ) !== -1;
                    }).attr('selected', true);  // Select given entry in the select
                    if ($(`${form_name} #${select_name} option`).length == 2) {
                        $(`${form_name} #${select_name}`).prop("selectedIndex", 1);
                    }
                    $(`${form_name} #${select_name}`).trigger('change');
                }
            } );
        }
    };

    addUpdDelButtonHandlers = function (tab_name) {
        // Add handlers to 'update' and 'delete' buttons for DataTable rows.
        // Buttons should exist at the moment of execution!
    
        // Update button
        $(`.js-update`).off('click');
        $(`.js-update`).click(function() {
            var dialog_id = $(this).closest('div.tab-pane').attr('dialog-id');
            var modal_id = loadForm2.call(this, 'update', dialog_id);
            $(modal_id).on('hidden.bs.modal', function() {
                $(modal_id).remove();  // Keep DOM clean!
            });  
        });
        // Delete button
        $(`.js-delete`).off('click');
        $(`.js-delete`).click(function() { 
            var modal_id = loadForm2.call(this, 'delete');
            $(modal_id).on('hidden.bs.modal', function() {
                $(modal_id).remove();  // Keep DOM clean!
            });  
        });
    };

    // Create button
    $('.js-create').click(function() {
        var dialog_id = $(this).closest('div.tab-pane').attr('dialog-id');
        var modal_id = loadForm2.call(this, 'create', dialog_id);
        $(modal_id).on('hidden.bs.modal', function() {
            $(modal_id).remove();  // Keep DOM clean!
        })
    });

    // Reload button
    $('.js-reload').click(function() { 
        $.fn.dataTable.tables( {visible: true, api: true} ).ajax.reload();
    });

    // Login
    $('.js-login').click(function() {
        var modal_name = getModalName();
        var modal_id = '#'+modal_name;
        addModal(modal_name, 'id_login_dialog');
        $.ajax({
            type: "get",
            url: $(this).attr("data-url"),
            dataType: 'html',
            success: function(data) {
                $(modal_id+' .modal-content').html(data);
                $(modal_id).modal('show');
            },
            error: function(xhr, errmsg, err) {
                console.error('Error occured when loading form data');
            }
        });
        $(modal_id).on('hidden.bs.modal', function() {
            $(modal_id).remove();  // Keep DOM clean!
        });  
    });
});