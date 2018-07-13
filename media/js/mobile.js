// jQuery-only functions

// TODO: tooltip links does not show link cursor if you hover.


// Set up event handlers
$(document).ready(function(){
	$('.feedback').hide();
	set_tooltip_hrefs();

	hide_settings_after_delay();

	$('input[type="text"]').keydown(next_field);
	$('input[type="text"]').click(insert_keys);
	$('a.link_tooltip').click(reveal_tooltip);
	$('a.feedback_link').click(reveal_feedback);
	
	$('select#id_semtype').change(function (e) {
			$('select#id_source').val('all') ;
			return false;
	});

	$('select#id_source').change(function (e) {
			$('select#id_semtype').val('all') ;
			return false;
	});
	
	$('select#grammarlink').change(function (e) {
			link = $('select#grammarlink#').val();
			window.open(link);
	});

	$('div#settings select').change(formsubmit);
	
	$('ul#opensettingsform a').click(toggle_settings);

	disable_autocomplete();

	$('.key').click(insertChar);
});

function insertChar(a) {
	character = $(a.target).html();

	target = $(a.target).parent().parent().parent().children('input[type="text"]');

	val = $(target).val();
	$(target).val(val + character);
	return false;
}

function insert_keys(e) {
	$('ul.keys').hide();
	// id_1-answer
	cur_id = e.target.id.match(/\d+/)[0];
	$('#keys-' + cur_id).show();

	return false;
}

function hide_settings_after_delay() {
	// #settingsform ul, #settingsform label
	$('#navbar').toggle();
	$('ul#settingsform').toggle();
	$('ul#opensettingsform').toggle();
}

function hide_settings() {
	$('#navbar').hide();
	$('ul#settingsform').hide();
	$('ul#opensettingsform').hide();
	$('#instructions').hide();
	$('div.grammarlinks').hide();
}

function toggle_settings() {
	$('#navbar').toggle();
	$('ul#settingsform').toggle();
	$('ul#opensettingsform').toggle();
	$('#instructions').toggle();
	$('div.grammarlinks').toggle();
}

function disable_autocomplete() {
	$('form#gameform')[0].setAttribute('autocomplete', 'off') ;

	for (var i = $('form#gameform input[type="text"]').length - 1; i >= 0; i--) {
		elem = $('form#gameform input[type="text"]')[i];
		elem.setAttribute('autocomplete', 'off') ;
	};

	return true; 
}

function set_tooltip_hrefs() {

	links = $('a.link_tooltip');

	for (var i = links.length - 1; i >= 0; i--) {
		link = links[i] ;

		link.setAttribute('href', '#');

	}

	return false;
}

function formsubmit (e) { 
	$('div#settings input[type="submit"]').click();
	$('input[type="submit"]').attr('disabled', 'disabled');
	return false;
}

function reveal_tooltip (event) {
	// $('#instructions').hide();
	reveal_id = event.target.id.match(/(tooltip-\d)/);
	$('.tooltip').hide();
	$('#' + reveal_id).show();
	return false; 
}

function reveal_feedback (event) {
	$('#instructions').hide() ;
	reveal_id = event.target.id.match(/(feedback-\d)/)[0];
	$('.tooltip').hide();
	$('#' + reveal_id).show();
	return false; 
}

// Switch to next field on enter, at end, go back to first empty field
// or focus test
function next_field (event) {
	if ((event.keyCode || event.which) == 13) {
		function first_empty (inputs) {
			return inputs[0];
		}
	
		current_id = event.target.id;
		match = current_id.match(/id_(\d)-answer/);
		count = parseFloat(match[1]) - 1;
		inputs = $('input[type="text"]');
	
		// Focus next
		$(inputs[count+1]).focus();
	
		if(count == 4){
			open_inputs = $("input:visible:enabled[type='text'][value='']").not(".nofocus");
			if (open_inputs.length == 0) {
				$('input[name="test"]').focus();
				return false;
			} else {
				open_inputs.slice(0, 1).focus();
				
			}
		}
		
		return false;
	}
	
}

function SetIndex(list,value) {
    if (value == "all") {
	   return;
    }
	if(list && list.options.length){ 
		for(var i=0; i<list.options.length; i++){ 
		if(list.options[i].value == "all"){ 
			list.selectedIndex = i; 
			return; 
			} 
		} 
	} 
}
	


// Non-jQuery functions that should probably be rewritten if they come into use.
//
// function selectsahka ( selectedtype )
// {
//     document.gameform.dialogue.value = selectedtype ;
//     document.gameform.submit() ;
// }


// function feedback(msg)
// {
//   var generator=window.open('','name','height=200,width=300');
//   generator.moveTo(50,50);
//   generator.document.write('<html><head><title>Tutorial</title>');
//   generator.document.write('</head><body>');
//   generator.document.write('<p>' + msg + '</p>');
//   generator.document.write('<p><a href="javascript:self.close()">close</a></p>');
//   generator.document.write('</body></html>');
//   generator.document.close();
// }


// function processvasta(event,form){
//     key = event.keyCode;
//     if (key==13){
//       form.submit();
//     }
//   }

// function sahkaSetFocus(){
// 
//   document.getElementByName('test').focus();
//   var node_list = document.getElementsByTagName('input');
// 	
//   for (var i = 0; i < node_list.length; i++) {
//     var node = node_list[i];
//     if (node.getAttribute('type') == 'text') {
//       node.focus();
//       }
//    }
// 
// } 

// function setFocus(form){
// 
//   if (form.gametype == "sahka") {
//     sahkaSetFocus();
//     return;
//   }
//   var node_list = document.getElementsByTagName('input');
//   var i=0;	
//   var found=0;
//   while (i < node_list.length & found==0) {
//     i++;
//     var node = node_list[i];
//     if (node.getAttribute('type') == 'text') {
//       node.focus();
//       found=1;
//     }
//   }
// } 


