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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
$(document).ready(function(){
    $('select[name=category]').html("<option value selected='selected'>בחר מקצוע כדי לבחור נושא</option>");
    $('select[name=subcategory]').html("<option value selected='selected'>בחר נושא כדי לבחור תת נושא</option>");
    $('select[name=subject]').change(function(){
        $('select[name=subcategory]').empty();
        $('select[name=category]').empty();
        subject_id = $(this).val();
        request_url = '/get_categories/' + subject_id + '/';
        $.ajax({
            url: request_url,
            dataType: "html",
            success: function(data){
                    $('select[name=category]').html(data);
                    $('select[name=category]').trigger("change");

            },
            error: function(data){
            $('select[name=category]').html("<option value selected='selected'>בחר מקצוע כדי לבחור נושא</option>");
            $('select[name=subcategory]').html("<option value selected='selected'>בחר נושא כדי לבחור תת נושא</option>");
            }
        })
    });
        $('select[name=category]').change(function(){
        category_id = $(this).val();
        request_url = '/get_subcategories/' + category_id + '/';
        $.ajax({
            url: request_url,
            dataType: "html",
            success: function(data){
                    $('select[name=subcategory]').html(data)

            }
        })
    });
});