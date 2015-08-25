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


function rateSummary(rate_type,rate_action,responseFunction){
    $.post(url,
    {id:id, type:rate_type, action:rate_action},
    function(response){
        if($.isNumeric(response)){
            responseFunction(response);
        }
    });   
}


$(document).ready(function(){
    positive_button = $('a.positive');
    negative_button = $('a.negative');

    positive_button.click(function(){
        var rate_type = 'positive';
        // the other rating button is already selected (negative --> positive)
        if(negative_button.hasClass('selected')){
            var rate_action = 'change-type';
            responseFunction = function(response){
                positive_button.addClass('selected');
                negative_button.removeClass('selected');
                // increment positive by 1
                var current_rating = positive_button.html().match(/\d+/);
                var new_rating = (parseInt(current_rating) + 1).toString();
                var newhtml = positive_button.html().replace(/\d+/, new_rating);
                positive_button.html(newhtml);
                // decrement negative by 1
                var current_rating = negative_button.html().match(/\d+/);
                var new_rating = (parseInt(current_rating) - 1).toString();
                var newhtml = negative_button.html().replace(/\d+/, new_rating);
                negative_button.html(newhtml);
            }
        }
        // the current rating button is already selected
        else if(positive_button.hasClass('selected')){
            var rate_action = 'undo-rate';
            responseFunction = function(response){
                positive_button.removeClass('selected');
                // replaces the rating number with the response (new rating number)
                var newhtml = positive_button.html().replace(/\d+/, response);
                positive_button.html(newhtml);
            }
        }
        // no rating button is selected
        else{
            var rate_action = 'rate';
            responseFunction = function(response){
                positive_button.addClass('selected');
                var newhtml = positive_button.html().replace(/\d+/, response);
                positive_button.html(newhtml);
            }
        }
    rateSummary(rate_type,rate_action,responseFunction);
    });

        negative_button.click(function(){
        var rate_type = 'negative';
        // the other rating button is already selected (negative --> positive)
        if(positive_button.hasClass('selected')){
            var rate_action = 'change-type';
            responseFunction = function(response){
                negative_button.addClass('selected');
                positive_button.removeClass('selected');
                // increment negative by 1
                var current_rating = negative_button.html().match(/\d+/);
                var new_rating = (parseInt(current_rating) + 1).toString();
                var newhtml = negative_button.html().replace(/\d+/, new_rating);
                negative_button.html(newhtml);
                // decrement positive by 1
                var current_rating = positive_button.html().match(/\d+/);
                var new_rating = (parseInt(current_rating) - 1).toString();
                var newhtml = positive_button.html().replace(/\d+/, new_rating);
                positive_button.html(newhtml);
            }
        }
        // the current rating button is already selected
        else if(negative_button.hasClass('selected')){
            var rate_action = 'undo-rate';
            responseFunction = function(response){
                negative_button.removeClass('selected');
                // replaces the rating number with the response (new rating number)
                var newhtml = negative_button.html().replace(/\d+/, response);
                negative_button.html(newhtml);
            }
        }
        // no rating button is selected
        else{
            var rate_action = 'rate';
            responseFunction = function(response){
                negative_button.addClass('selected');
                var newhtml = negative_button.html().replace(/\d+/, response);
                negative_button.html(newhtml);
            }
        }
    rateSummary(rate_type,rate_action,responseFunction);
    });
});

