$(function() {
    load_form = function (modal_name) {
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
                $(modal_name+' .modal-content').html(xhr.responseText);
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    };

    save_form = function(e, modal_name) {
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
                    $(modal_name).modal('hide');
                }
                else {
                    $(modal_name+' .modal-content').html(data.html_form);
                }
            },
            error: function(xhr, errmsg, err) {
                $(modal_name+' .modal-content').html(xhr.responseText);
                console.log(xhr.status + ": " + xhr.responseText);
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
            load_form.call(this, modal_name);
        });
        $(modal_name).on('submit', '.js-collection-update-form', function(e) {
            save_form.call(this, e, modal_name);
        });
    
        // Delete collection
        $('.js-delete-collection').click(function() { 
            load_form.call(this, modal_name);
        });
        $(modal_name).on('submit', '.js-collection-delete-form', function(e) {
            save_form.call(this, e, modal_name);
        });
    };
    
    addDatasetButtonHandlers = function () {
        // Add handlers to 'update' and 'delete' buttons for Dataset rows.
        // Buttons should exist at the moment of execution!
    
        var modal_name = '#modal-dataset';
    
        // Update dataset
        $('.js-update-dataset').click(function() { 
            load_form.call(this, modal_name);
        });
        $(modal_name).on('submit', '.js-dataset-update-form', function(e) {
            save_form.call(this, e, modal_name);
        });
    
        // Delete dataset
        $('.js-delete-dataset').click(function() { 
            load_form.call(this, modal_name);
        });
        $(modal_name).on('submit', '.js-dataset-delete-form', function(e) {
            save_form.call(this, e, modal_name);
        });
    };
    
    addDataButtonHandlers = function () {
        // Add handlers to 'update' and 'delete' buttons for Data rows.
        // Buttons should exist at the moment of execution!
    
        var modal_name = '#modal-data';
    
        // Update data
        $('.js-update-data').click(function() { 
            load_form.call(this, modal_name);
        });
        $(modal_name).on('submit', '.js-data-update-form', function(e) {
            save_form.call(this, e, modal_name);
        });
    
        // Delete data
        $('.js-delete-data').click(function() { 
            load_form.call(this, modal_name);
        });
        $(modal_name).on('submit', '.js-data-delete-form', function(e) {
            save_form.call(this, e, modal_name);
        });
    };

    // Create collection
    var modal_name = '#modal-collection';
    $('.js-create-collection').click(function() { 
        load_form.call(this, modal_name);
    });
    $(modal_name).on('submit', '.js-collection-create-form', function(e) {
        save_form.call(this, e, modal_name);
    });

    // Create dataset
    var modal_name = '#modal-dataset';
    $('.js-create-dataset').click(function() { 
        load_form.call(this, modal_name);
    });
    $(modal_name).on('submit', '.js-dataset-create-form', function(e) {
        save_form.call(this, e, modal_name);
    });
    
    // Create data
    var modal_name = '#modal-data';
    $('.js-create-data').click(function() { 
        load_form.call(this, modal_name);
    });
    $(modal_name).on('submit', '.js-data-create-form', function(e) {
        save_form.call(this, e, modal_name);
    });
});