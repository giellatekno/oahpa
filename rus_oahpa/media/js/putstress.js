$(function add_stress () {
    $('.click-to-stress').click(
	function () {
	    previous_input_box = $(this).prevAll('input').last();
	    if (previous_input_box.length == 0) {
		previous_input_box = $(this).prevAll('span .incorrect').last().children('input').last();
	    };
	    current_text = previous_input_box.attr('value');
	    previous_input_box.attr('value', current_text + "́");
	    previous_input_box.focus();
	});
})
