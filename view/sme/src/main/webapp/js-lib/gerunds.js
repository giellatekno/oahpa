
	wertiview.gerunds = {

	//MAX_CLOZE: 25,
	
	remove: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		$('body').undelegate('span.wertiviewtoken', 'click', wertiview.gerunds.clickHandler);
		$('body').undelegate('select.wertiviewinput', 'change', wertiview.gerunds.clozeInputHandler);
		$('body').undelegate('span.wertiviewhint', 'click', wertiview.gerunds.clozeHintHandler);
		$('body').undelegate('input.wertiviewinput', 'change', wertiview.gerunds.clozeInputHandler);
		$('body').undelegate('span.wertiviewhint', 'click', wertiview.gerunds.clozeHintHandler);
		
		$('.wertiviewinput').each( function() {
			$(this).replaceWith($(this).data('wertiviewanswer'));
		});
		$('span.wertiviewbaseform').remove();
		$('.wertiviewhint').remove();
	},

	colorize: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		$('span.wertiviewGER').addClass('colorizeStyleGER');
		$('span.wertiviewINF').addClass('colorizeStyleINF');
		$('span.wertiviewINFSPLIT').addClass('colorizeStyleINFSPLIT');
		$('span.wertiviewCLU-GERONLY, span.wertiviewCLU-INFONLY, span.wertiviewCLU-BOTHMEANSAME, span.wertiviewCLU-BOTHMEANDIFF, span.wertiviewCLU-FIXEDEXP').addClass('colorizeStyleCLU');
	},
	
	colorizeSpan: function(span, topic) {
		span.find('span.wertiviewGER').addClass('colorizeStyleGER');
		span.find('span.wertiviewINF').addClass('colorizeStyleINF');
		span.find('span.wertiviewINFSPLIT').addClass('colorizeStyleINFSPLIT');
		span.find('span.wertiviewCLU-GERONLY, span.wertiviewCLU-INFONLY, span.wertiviewCLU-BOTHMEANSAME, span.wertiviewCLU-BOTHMEANDIFF, span.wertiviewCLU-FIXEDEXP').addClass('colorizeStyleCLU');
	},

	click: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		// change all wertiviewtoken spans to mouseover pointer
		$('span.wertiviewtoken').css({'cursor': 'pointer'});

		// gerund and infinitive markup
		$('span.wertiviewRELEVANT').find('span.wertiviewGER').addClass('colorizeStyleGER');
		$('span.wertiviewRELEVANT').find('span.wertiviewINF').addClass('colorizeStyleINF');

		// correct cursor inside wertiviewtokens within multi-word spans
		$('span.wertiviewRELEVANT').find('span.wertiviewGER, span.wertiviewINF').css({'cursor': 'text'});
		$('span.wertiviewRELEVANT').find('span.wertiviewINF').children().css({'cursor': 'text'});

		// handle clue click
		$('body').delegate('span.wertiviewtoken', 'click', {context: contextDoc}, wertiview.gerunds.clickHandler);
	},

	clickHandler: function(event) {
		var contextDoc = event.data.context;

		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		$(this).css({'cursor': 'auto'});
        
		// not within a relevant phrase
		if ($(this).parents('.wertiviewRELEVANT').length == 0) {
			$(this).addClass('clickStyleIncorrect');
			return false;
		}

		// an already colored gerund or infinitive
		var isColored = false;

		if ($(this).hasClass('wertiviewGER') || $(this).hasClass('wertiviewINF') || $(this).find('.wertiviewGER, .wertiviewINF').length > 0) {
			isColored = true;
		}

		if (isColored) {
			return false;
		}

		// if this is a clue
		var isClue = false;

		if ($(this).hasClass('wertiviewCLU-BOTHMEANDIFF') || $(this).hasClass('wertiviewCLU-BOTHMEANSAME') || 
				$(this).hasClass('wertiviewCLU-FIXEDEXP') || $(this).hasClass('wertiviewCLU-GERONLY') || 
				$(this).hasClass('wertiviewCLU-INFONLY') || 
				$(this).find('.wertiviewCLU-BOTHMEANDIFF, .wertiviewCLU-BOTHMEANSAME, .wertiviewCLU-FIXEDEXP, .wertiviewCLU-GERONLY, .wertiviewCLU-INFONLY').length > 0) {
			isClue = true;
		}
		
		if (isClue) {
			$(this).addClass('clickStyleCorrect');
		} else {
			$(this).addClass('clickStyleIncorrect');
		}
		return false;
	},
	
	mc: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		// get potential spans
		var $hits = $('span.wertiviewRELEVANT').find('span.wertiviewGER,span.wertiviewINF');
		
		var hitList = []; 
		$hits.each( function() {
			// if this is a split infinitive, skip
			if ($(this).find('.wertiviewINFSPLIT').length == 0) {
				var options = $(this).attr('title').split(";");
				// if the infinitive or gerund isn't given in the markup, skip
				for (var j = 0; j < options.length; j++) {
					if (options[j] == 'null') {
						return;
					}
				}
				hitList.push($(this));				
			}
		});

		wertiview.activity.mc(contextDoc, hitList, 
				wertiview.gerunds.clozeInputHandler, 
				wertiview.gerunds.clozeHintHandler, 
				wertiview.gerunds.mcGetOptions, 
				wertiview.gerunds.mcGetCorrectAnswer);

	},
	
	mcGetOptions: function($hit, capType){
		var options = $hit.attr('title').split(";");
		return options;
	},
	
	mcGetCorrectAnswer: function($hit, capType){
		return $hit.text();
	},
	
	cloze: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		// get potential spans
		var $hits = $('span.wertiviewRELEVANT').find('span.wertiviewGER,span.wertiviewINF');

		var hitList = []; 
		$hits.each( function() {
			// if this is a split infinitive, skip
			if ($(this).find('.wertiviewINFSPLIT').length == 0) {
				hitList.push($(this));				
			}
		});

		wertiview.activity.cloze(contextDoc, hitList, 
				wertiview.gerunds.clozeInputHandler, 
				wertiview.gerunds.clozeHintHandler, 
				wertiview.gerunds.mcGetCorrectAnswer,
				wertiview.gerunds.clozeAddBaseform);
	},
	
	clozeAddBaseform: function($hit, capType, $){
		// create baseform info
		var $baseform = $('<span>');
		$baseform.addClass('clozeStyleBaseform');
		$baseform.addClass('wertiviewbaseform');
		var verbforms = $hit.attr('title').split(';');
		$baseform.text(' (' + verbforms[0] + ')');
		$hit.append($baseform);	
	},

	clozeInputHandler: function(event) {
		var jQuery = wertiview.jQuery;
		var contextDoc = event.data.context;
		  var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		  $.fn = $.prototype = jQuery.fn;

		var nextInput;

		// if the answer is correct, turn into text, else color text within input
		if($(this).val().toLowerCase() == $(this).data('wertiviewanswer').toLowerCase()) {
			$text = $("<span>");
			$text.addClass('wertiview');
			$text.addClass('clozeStyleCorrect');
			$text.text($(this).data('wertiviewanswer'));
			if($(this).data('wertiviewnexthit')) {
				nextInput = $(this).data('wertiviewnexthit');
			}
			wertiview.lib.replaceInput($(this).parent(), $text);

			/*// focus next input
			if(nextInput) {
				$("#" + nextInput).get(0).focus();
			}*/
		} else {
			$(this).addClass('clozeStyleIncorrect');
		}
	},

	clozeHintHandler: function(event) {
		var jQuery = wertiview.jQuery;
		var contextDoc = event.data.context;
		  var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		  $.fn = $.prototype = jQuery.fn;

		var nextInput;

		// fill in the answer by replacing input with text
		$text = $("<span>");
		$text.addClass('wertiview');
		$text.addClass('clozeStyleProvided');
		$text.text($(this).prev().data('wertiviewanswer'));
		if($(this).prev().data('wertiviewnexthit')) {
			nextInput = $(this).prev().data('wertiviewnexthit');
		}
		wertiview.lib.replaceInput($(this).parent(), $text);

		/*// focus next input
		if(nextInput) {
			$("#" + nextInput).get(0).focus();
		}*/
		
		return false;
	}
	};

