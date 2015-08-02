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

	$(document).ready(function() {
		if($('a.negative').hasClass('selected')){
			$('a.negative img').attr("src", '/static/images/negative_selected.svg');
		}
		else if($('a.positive').hasClass('selected')){
			$('a.positive img').attr("src", '/static/images/positive_selected.svg');
		}

	$('a.positive').click(function(){
		if($('a.negative').hasClass('selected')){
			$( "a.negative" ).trigger( "click" );
		}
		var rate_type = 'positive';
		if($(this).hasClass('selected')){
			var rate_action = 'undo-rate';
			$.post(url,
			{id:id, type:rate_type, action:rate_action},
			function(response){
				if($.isNumeric(response)){
					$('a.positive').removeClass('selected')
					.html('<img height="25" width="25" src="/static/images/positive.svg" %}">אהבתי  ('+response+')');
				}
			});
		} 
		else{
			var rate_action = 'rate';
			$.post(url,
			{id:id, type:rate_type, action:rate_action},
			function(response){
				if($.isNumeric(response)){
					$('a.positive').addClass('selected')
					.html('<img height="25" width="25" src="/static/images/positive_selected.svg">אהבתי  ('+response+')');
				}
			});

		}
	});
		$('a.negative').click(function(){
		if($('a.positive').hasClass('selected')){
			$( "a.positive" ).trigger( "click" );
		}
		var rate_type = 'negative';
		if($(this).hasClass('selected')){
			var rate_action = 'undo-rate';
			$.post(url,
			{id:id, type:rate_type, action:rate_action},
			function(response){
				if($.isNumeric(response)){
					$('a.negative').removeClass('selected')
					.html('<img height="25" width="25" src="/static/images/negative.svg" %}">לא משהו  ('+response+')');
				}
			});
		} 
		else{
			var rate_action = 'rate';
			$.post(url,
			{id:id, type:rate_type, action:rate_action},
			function(response){
				if($.isNumeric(response)){
					$('a.negative').addClass('selected')
					.html('<img height="25" width="25" src="/static/images/negative_selected.svg" %}">לא משהו  ('+response+')');
				}
			});

		}
	});
});
