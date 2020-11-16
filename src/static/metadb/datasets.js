$(function() {
    load_dataset_form = function () {
        var btn = $(this);
        $.ajax({
            type: "get",
            url: btn.attr("data-url"),
            dataType: 'json',
            beforeSend: function() {
                $('#modal-dataset').modal('show');
            },
            success: function(data) {
                $('#modal-dataset .modal-content').html(data.html_form)
            },
            error: function(xhr, errmsg, err) {
//                $("#modal-dataset .modal-content").html(xhr.responseText);
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    };

    save_dataset_form = function(e) {
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
                    $('#modal-dataset').modal('hide');
                }
                else {
                    $("#modal-dataset .modal-content").html(data.html_form);
                }
            },
            error: function(xhr, errmsg, err) {
//                $("#modal-dataset .modal-content").html(xhr.responseText);
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
        return false;
    };

    // Create dataset
    $('.js-create-dataset').click(load_dataset_form);
    $('#modal-dataset').on('submit', '.js-dataset-create-form', save_dataset_form);





    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});