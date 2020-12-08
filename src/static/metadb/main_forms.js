$(function() {

    var addModal = function(modal_name) {
        if (!$('#'+modal_name).length) {
            var modal = $('<div class="modal fade" tabindex="-1" role="dialog">');
            modal.attr('id', modal_name);
            var modal_dialog = $('<div class="modal-dialog" role="document">');
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
        return 'modal-dynamic-'+idx;
    };

    loadForm2 = function () {
        var btn = $(this);
        var modal_name = getModalName();
        addModal(modal_name);
        var modal_id = '#'+modal_name;
        $.ajax({
            type: "get",
            url: btn.attr("data-url"),
            dataType: 'json',
            beforeSend: function() {
                $(modal_id).modal('show');
            },
            success: function(data) {
                $(modal_id+' .modal-content').html(data.html_form)
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

        $.ajax({
            type: form.attr('method'),
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
                console.error('Error occured when saving form data');
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

    loadOptions = function(form_name, select_name, data_url, option_name='') {
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

    addUpdDelButtonHandlers = function (tab_name) {
        // Add handlers to 'update' and 'delete' buttons for DataTable rows.
        // Buttons should exist at the moment of execution!
    
        // Update button
        $(`.js-update-${tab_name}`).off('click');
        $(`.js-update-${tab_name}`).click(function() { 
            var modal_id = loadForm2.call(this);
            $(modal_id).on('hidden.bs.modal', function() {
                $(modal_id).remove();  // Keep DOM clean!
            });  
        });
        $('body').off('submit', `.js-${tab_name}-form`);
        $('body').on('submit', `.js-${tab_name}-form`, function(e) {
            saveForm2.call(this, e); return false;
        });
        // Delete button
        $(`.js-delete-${tab_name}`).off('click');
        $(`.js-delete-${tab_name}`).click(function() { 
            var modal_id = loadForm2.call(this);
            $(modal_id).on('hidden.bs.modal', function() {
                $(modal_id).remove();  // Keep DOM clean!
            });  
        });
        $('body').off('submit', `.js-${tab_name}-delete-form`);
        $('body').on('submit', `.js-${tab_name}-delete-form`, function(e) {
            saveForm2.call(this, e); return false;
        });
    };

    // Create button
    $('.js-create').click(function() { 
        var modal_id = loadForm2.call(this);
        $(modal_id).on('hidden.bs.modal', function() {
            $(modal_id).remove();  // Keep DOM clean!
        })
    });

});