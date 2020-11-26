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

    addCollectionButtonHandlers = function () {
        // Add handlers to 'update' and 'delete' buttons for Collection rows.
        // Buttons should exist at the moment of execution!
    
        var modal_name = '#modal-collection';
    
        // Update collection
        $('.js-update-collection').click(function() { 
            loadForm.call(this, modal_name);
        });
        $(modal_name).on('submit', '.js-collection-update-form', function(e) {
            saveForm.call(this, e, modal_name); return false;
        });
    
        // Delete collection
        $('.js-delete-collection').click(function() { 
            loadForm.call(this, modal_name);
        });
        $(modal_name).on('submit', '.js-collection-delete-form', function(e) {
            saveForm.call(this, e, modal_name); return false;
        });
    };
    
    addDatasetButtonHandlers = function () {
        // Add handlers to 'update' and 'delete' buttons for Dataset rows.
        // Buttons should exist at the moment of execution!
    
        var modal_name = '#modal-dataset';
    
        // Update dataset
        $('.js-update-dataset').click(function() { 
            loadForm.call(this, modal_name);
        });
        $(modal_name).on('submit', '.js-dataset-update-form', function(e) {
            saveForm.call(this, e, modal_name); return false;
        });
    
        // Delete dataset
        $('.js-delete-dataset').click(function() { 
            loadForm.call(this, modal_name);
        });
        $(modal_name).on('submit', '.js-dataset-delete-form', function(e) {
            saveForm.call(this, e, modal_name); return false;
        });
    };
    
    addDataButtonHandlers = function () {
        // Add handlers to 'update' and 'delete' buttons for Data rows.
        // Buttons should exist at the moment of execution!
    
        var modal_name = '#modal-data';
    
        // Update data
        $('.js-update-data').click(function() { 
            loadForm.call(this, modal_name);
        });
        $(modal_name).on('submit', '.js-data-update-form', function(e) {
            saveForm.call(this, e, modal_name); return false;
        });
    
        // Delete data
        $('.js-delete-data').click(function() { 
            loadForm.call(this, modal_name);
        });
        $(modal_name).on('submit', '.js-data-delete-form', function(e) {
            saveForm.call(this, e, modal_name); return false;
        });
    };

    // Create collection button
    $('.js-create-collection').click(function() { 
        loadForm.call(this, '#modal-collection');
    });
    $('#modal-collection').on('submit', '.js-collection-create-form', function(e) {
        saveForm.call(this, e, '#modal-collection'); return false; 
    });

    // Create dataset button
    $('.js-create-dataset').click(function() { 
        loadForm.call(this, '#modal-dataset');
    });
    $('#modal-dataset').on('submit', '.js-dataset-create-form', function(e) {
        saveForm.call(this, e, '#modal-dataset'); return false;
    });
    
    // Create data button
    $('.js-create-data').click(function() { 
        loadForm.call(this, '#modal-data');
    });
    $('#modal-data').on('submit', '.js-data-create-form', function(e) {
        saveForm.call(this, e, '#modal-data'); return false;
    });

    // Create another modal button
    $('body').on('click', '.js-add-button', function() { 
        loadForm.call(this, '#modal-over');
    });
});