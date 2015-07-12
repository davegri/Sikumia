$(document).ready(function() {
	$('a.positive').click(function(){
		var id = {{ summary.id }};
		var rate_type = 'positive';

		if($(this).hasClass('selected')){
			var rate_action = 'undo-vote';
			$.post({% static 'rate_summary' %},
			{id:id, type:rate_type, action:rate_action},
			function(response){
				if(isInt(response)){
					.removeClass('selected');
				}
			});
		}
	});
});