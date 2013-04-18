wertiview.ns(function() {
	wertiview.konjunktiv = {	

	// for documentation of these variables, see pos.js
	MAX_MC: 5,
	maxLength: 5,

	types: [],
	
	remove: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		$('body').undelegate('span.wertiviewtoken', 'click', wertiview.konjunktiv.clickHandler);
		$('body').undelegate('select.wertiviewinput', 'change', wertiview.konjunktiv.clozeInputHandler);
		$('body').undelegate('span.wertiviewhint', 'click', wertiview.konjunktiv.clozeHintHandler);
		$('body').undelegate('input.wertiviewinput', 'change', wertiview.konjunktiv.clozeInputHandler);
		$('body').undelegate('input.wertiviewhint', 'click', wertiview.konjunktiv.clozeHintHandler);

		$('.wertiviewinput').each( function() {
			$(this).replaceWith($(this).data('wertiviewanswer'));
		});
		$('.wertiviewhint').remove();
	},

	colorize: function(contextDoc) {
		var jQuery = wertiview.jQuery;
        var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
        $.fn = $.prototype = jQuery.fn;        
        
		$('span.wertiviewkonj1').addClass('colorizeStyleKonjunktiv1');
		$('span.wertiviewkonj2').addClass('colorizeStyleKonjunktiv2');
	},
	
	colorizeSpan: function(span, topic, index) {
		span.find('span.wertiviewkonj1').addClass('colorizeStyleKonjunktiv1');
		span.find('span.wertiviewkonj2').addClass('colorizeStyleKonjunktiv2');
	},
	
	click: function(contextDoc) {
		var jQuery = wertiview.jQuery;
                var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
                $.fn = $.prototype = jQuery.fn;

		// change all wertiviewtoken spans to mouseover pointer
		$('span.wertiviewtoken').css({'cursor': 'pointer'});

		// handle POS clicking
		$('body').delegate('span.wertiviewtoken', 'click', {context: contextDoc}, wertiview.konjunktiv.clickHandler);
	},

	clickHandler: function(event) {
		var jQuery = wertiview.jQuery;
		var contextDoc = event.data.context;
        var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
        $.fn = $.prototype = jQuery.fn;
                
		if($(this).hasClass('wertiviewkonjfin')) {
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
		var $hits = $('span.wertiviewkonjfin.wertiviewkonjaux');
		
		var hitList = [];
		var tokens = [];
		wertiview.konjunktiv.types = [];
		$hits.each( function() {
			hitList.push($(this));
			tokens[$(this).text().toLowerCase()] = 1;
		});
		for (word in tokens) {
			wertiview.konjunktiv.types.push(word);
		}
		
		wertiview.konjunktiv.maxLength = wertiview.konjunktiv.MAX_MC;
		if (wertiview.konjunktiv.maxLength > wertiview.konjunktiv.types.length) {
			wertiview.konjunktiv.maxLength = wertiview.konjunktiv.types.length;
		}
		
		wertiview.activity.mc(contextDoc, hitList, 
				wertiview.konjunktiv.clozeInputHandler, 
				wertiview.konjunktiv.clozeHintHandler, 
				wertiview.konjunktiv.mcGetOptions, 
				wertiview.konjunktiv.mcGetCorrectAnswer);
	},
	
	mcGetOptions: function($hit, capType){
		wertiview.lib.shuffleList(wertiview.konjunktiv.types);
		
		var options = [];
		var j = 0;
		while (options.length < wertiview.konjunktiv.maxLength - 1) {
			if (wertiview.konjunktiv.types[j] != $hit.text().toLowerCase()) {
				options.push(wertiview.lib.matchCapitalization(wertiview.konjunktiv.types[j], capType));
			}
			j++;
		}
		
		options.push(wertiview.lib.matchCapitalization($hit.text(), capType));
		
		wertiview.lib.shuffleList(options);
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
		var $hits = $('span.wertiviewkonjfin.wertiviewkonjaux');
		
		var hitList = []; 
		$hits.each( function() {
			hitList.push($(this));				
		});

		wertiview.activity.cloze(contextDoc, hitList, 
				wertiview.konjunktiv.clozeInputHandler, 
				wertiview.konjunktiv.clozeHintHandler, 
				wertiview.konjunktiv.mcGetCorrectAnswer);
	},

	clozeInputHandler: function(event) {
		var contextDoc = event.data.context;
		
		var jQuery = wertiview.jQuery;
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
		
		return false;
	},

	clozeHintHandler: function(event) {
		var contextDoc = event.data.context;
		
		var jQuery = wertiview.jQuery;
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
		if(nextInput && $("#" + nextInput).length == 1) {
			$("#" + nextInput).get(0).focus();
		}*/
		
		return false;
	}
	};
}); // REMOVE-WITH-MAVEN-REPLACER-PLUGIN
