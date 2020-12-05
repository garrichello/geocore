$(function() {
    loadForm = function (modal_name) {
        var btn = $(this);
        $.ajax({
            type: "get",
            url: btn.attr("data-url"),
            dataType: 'json',
            beforeSend: function() {
                $(modal_name).modal('show');
            },
            success: function(data) {
                $(modal_name+' .modal-content').html(data.html_form)
            },
            error: function(xhr, errmsg, err) {
                console.error('Error occured when loading form data');
//                $(modal_name+' .modal-content').html(xhr.responseText);
//                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    };

    saveForm = function(e, modal_name) {
        e.stopImmediatePropagation();
        var form = $(this);
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            dataType: 'json',
            success: function(data) {
                if (data.form_is_valid) {
                    $.fn.dataTable.tables( {visible: false, api: true} ).ajax.reload();
                }
                else {
                    $(modal_name+' .modal-content').html(data.html_form);
                }
            },
            error: function(xhr, errmsg, err) {
                console.error('Error occured when saving form data');
//                $(modal_name+' .modal-content').html(xhr.responseText);
//                console.log(xhr.status + ": " + xhr.responseText);
            },
            complete: function() {
                $(modal_name).modal('hide');
            }
        });
        return false;
    };

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

    getModalName = function(url) {
        return 'modal-dynamic-'+url.replaceAll('/', '');
    };

    loadForm2 = function () {
        var btn = $(this);
        var modal_name = getModalName(btn.attr("data-url"));
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
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
        return modal_id;
    };

    saveForm2 = function(e) {
        e.stopImmediatePropagation();
        var form = $(this);
        var modal_id = '#'+getModalName(form.attr('action'));
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            dataType: 'json',
            success: function(data) {
                if (data.form_is_valid) {
                    $.fn.dataTable.tables( {visible: false, api: true} ).ajax.reload();
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
            complete: function() {
                $(modal_id).modal('hide');
            }
        });
    };

    mapFormData = function(form_class) {
        var form_data = $(form_class).serializeArray().reduce(function(obj, item) {
            obj[item.name] = item.value;
            return obj;
        }, {});
        return form_data;
    };

    addCollectionButtonHandlers = function () {
        // Add handlers to 'update' and 'delete' buttons for Collection rows.
        // Buttons should exist at the moment of execution!
    
        // Update collection
        $('.js-update-collection').click(function() { 
            var modal_id = loadForm2.call(this);
            $(modal_id).on('hidden.bs.modal', function() {
                $(modal_id).remove();  // Keep DOM clean!
            });  
        });
        $('body').on('submit', '.js-collection-update-form', function(e) {
            saveForm2.call(this, e); return false;
        });
    
        // Delete collection
        $('.js-delete-collection').click(function() { 
            var modal_id = loadForm2.call(this);
            $(modal_id).on('hidden.bs.modal', function() {
                $(modal_id).remove();  // Keep DOM clean!
            });  
        });
        $('body').on('submit', '.js-collection-delete-form', function(e) {
            saveForm2.call(this, e); return false;
        });
    };
    
    addDatasetButtonHandlers = function () {
        // Add handlers to 'update' and 'delete' buttons for Dataset rows.
        // Buttons should exist at the moment of execution!
      
        // Update dataset
        $('.js-update-dataset').click(function() { 
            var modal_id = loadForm2.call(this);
            $(modal_id).on('hidden.bs.modal', function() {
                $(modal_id).remove();  // Keep DOM clean!
            });  
        });
        $('body').on('submit', '.js-dataset-update-form', function(e) {
            saveForm2.call(this, e); return false;
        });
    
        // Delete dataset
        $('.js-delete-dataset').click(function() { 
            var modal_id = loadForm2.call(this);
            $(modal_id).on('hidden.bs.modal', function() {
                $(modal_id).remove();  // Keep DOM clean!
            });  
        });
        $('body').on('submit', '.js-dataset-delete-form', function(e) {
            saveForm2.call(this, e); return false;
        });
    };
    
    addDataButtonHandlers = function () {
        // Add handlers to 'update' and 'delete' buttons for Data rows.
        // Buttons should exist at the moment of execution!
        
        // Update data
        $('.js-update-data').click(function() { 
            var modal_id = loadForm2.call(this);
            $(modal_id).on('hidden.bs.modal', function() {
                $(modal_id).remove();  // Keep DOM clean!
            });  
        });
        $('body').on('submit', '.js-data-update-form', function(e) {
            saveForm2.call(this, e); return false;
        });
    
        // Delete data
        $('.js-delete-data').click(function() { 
            var modal_id = loadForm2.call(this);
            $(modal_id).on('hidden.bs.modal', function() {
                $(modal_id).remove();  // Keep DOM clean!
            });  
        });
        $('body').on('submit', '.js-data-delete-form', function(e) {
            saveForm2.call(this, e); return false;
        });
    };

    // Create collection
    $('.js-create-collection').click(function() { 
        var modal_id = loadForm2.call(this);
        $(modal_id).on('hidden.bs.modal', function() {
            $(modal_id).remove();  // Keep DOM clean!
        })
    });

    // Create dataset
    $('.js-create-dataset').click(function() { 
        var modal_id = loadForm2.call(this);
        $(modal_id).on('hidden.bs.modal', function() {
            $(modal_id).remove();  // Keep DOM clean!
        })
    });
    
    // Create data
    $('.js-create-data').click(function() { 
        var modal_id = loadForm2.call(this);
        $(modal_id).on('hidden.bs.modal', function() {
            $(modal_id).remove();  // Keep DOM clean!
        })
    });
});