// jQuery-only functions

// TODO: tooltip links does not show link cursor if you hover.

function tillatpopup() {
    //document.write(navigator.userAgent)
    var browser ;
    browser = navigator.userAgent;
    if (browser.search("Safari")>0 && browser.search("Version/5.1")>0) 
    {
        var mine; 
        mine = window.open('','','width=1, height=1, left=0, top=0, scrollbars=no, titlebar=no, toolbar=no,status=no,resizable=no');
        if (!mine) {
            alert('Tillat popup-vinduer for å se grammatikkforklaringer.');
        } else {
        	mine.close();    
        }
    }
    return true ;
}

function prependTest () {
  var test_banner;
  test_banner = $('<div id="test_banner" />');
  test_banner.css({
    "position": "absolute",
    "top": "-2em",
    "left": "-5em",
    "z-index": "-1",
    "background-color": "blue",
    "color": "white",
    "letter-spacing": "1px",
    "padding": "5em 4em 1em 5em",
    "-webkit-transform": "rotate(-45deg)",
    "border-bottom": "5px solid #4A4"
  }).text("Testing!");
  return $("body").prepend(test_banner);
};


// Set up event handlers
$(document).ready(function(){
	tillatpopup() ;
	$('.feedback').hide();
	set_tooltip_hrefs();

	$('input[type="text"]').keydown(next_field);
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
			return false;
	});

	$('select[name="possessive_type"]').change(function (e) {
		$('select[name="possessive_case"]')[0].value = '';
	});

	$('div#settings select').change(formsubmit);
    
    $('.interface').mouseenter(translate);
    $('.interface').mouseleave(restore_attr);

	if (window.location.host == "testing.oahpa.no") {
    	prependTest() ;
    }

	disable_autocomplete();
});


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

//function disable_submit(e) {
	//$('input[type="submit"]').attr('disabled', 'true');
	//e.target.submit() ;
//}


function formsubmit (e) { 
	$('div#settings input[type="submit"]').click();
	$('input[type="submit"]').attr('disabled', 'disabled');
	return false;
}

function reveal_tooltip (event) {
	reveal_id = event.target.id.match(/(tooltip-\d)/);
	$('.tooltip').hide();
	$('#' + reveal_id).show();
	return false; 
}

function reveal_feedback (event) {
	/* Somehow JS seems to be thinking the <t /> node is the event target
	   so, now we need to get the parent of the event that is a.feedback_link.
	*/
	feedback_link = $(event.target).parents('a.feedback_link')[0];
	reveal_id = feedback_link.id.match(/(feedback-\d)/);

	$('div.language_help').hide()
	$('.tooltip').hide();
	$('#' + reveal_id).show();

    // If the Google isn't with us, skip the rest.
    // if (typeof _gaq !== "undefined" && _gaq !== null) {
    // 	return false ;
    // }

	var feedback_event_desc = $('#' + reveal_id).html().replace(/\n/g, ' ').replace(/ [ ]*/g, ' ') ;

	// Figure out what the form select element is, and also thus what the exercize is.
	var morfas_type_form = [ 'form select[name="case"]'
	                       , 'form select[name="vtype"]'
	                       , 'form select[name="adjcase"]'
	                       , 'form select[name="num_bare"]'
	                       , 'form select[name="pron_type"]'
	                       , 'form select[name="derivation_type"]'
	                       , 'form select[name="possessive_case"]'
	                       ] ;

    morfas_elem = false;
    for (_i = 0, _len = morfas_type_form.length; _i < _len; _i++) {
        a = morfas_type_form[_i];
        if ($(a).length > 0) {
            morfas_elem = $(a);
        }
    }


	// also for morfac, separately.
	// NB: the names of these are sometimes different from the name of those above
	var morfac_type_form = [ 'form select[name="case_context"]'
	                       , 'form select[name="vtype_context"]'
	                       , 'form select[name="adjcase_context"]'
	                       , 'form select[name="num_bare_context"]'
	                       , 'form select[name="pron_context"]'
	                       , 'form select[name="derivation_type_context"]'
	                       , 'form select[name="possessive_case_context"]'
                           ] ;

    morfac_elem = false;
    for (_i = 0, _len = morfac_type_form.length; _i < _len; _i++) {
        a = morfac_type_form[_i];
        if ($(a).length > 0) {
            morfac_elem = $(a);
        }
    }

    if (typeof morfas_elem !== "undefined" && morfas_elem !== null) {
        var game_type = morfas_elem.val()
          , game_name = "MorfaS"
          ;
    } else if (typeof morfac_elem !== "undefined" && morfac_elem !== null) {
        var game_type = morfac_elem.val()
          , game_name = "MorfaC"
          ;
    }

    var event_title = game_name + " " + game_type 
      ,  event_type = "FeedbackClick" 
      ;

    var google_event_args = ['_trackEvent', event_type, event_title, feedback_event_desc];

    _gaq.push(google_event_args)
    //
    // TODO: feedback tracking
    //
    // waiting to see some test events in analytics data to make sure it works, then will
    // write the code
    //
	return false; 
}

// Create a localisation tooltip for the text on HTML elements with class 
// "interface" when ALT key is hold down and mouse enteres the HTML element
function translate(event) {  
    if (event.altKey || event.altLeft) {
        $(this).children('span').removeAttr('class');
        $(this).children('span').setAttribute('class',"shortinfo_lang");      
    }
}

function restore_attr(event) {
    $(this).children('span').setAttribute('class',"invisible");
    this.setAttribute('class',"interface");    
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


