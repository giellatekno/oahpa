wertiview.ns(function() {
	wertiview.phrasalverbs = {
	
	// for documentation of these variables, see pos.js
	MAX_MC: 5,
	maxLength: 5,
	
	types: [],
	
	remove: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		$('body').undelegate('span.wertiviewtoken', 'click', wertiview.phrasalverbs.clickHandler);
		$('body').undelegate('select.wertiviewinput', 'change', wertiview.phrasalverbs.clozeInputHandler);
		$('body').undelegate('span.wertiviewhint', 'click', wertiview.phrasalverbs.clozeHintHandler);
		$('body').undelegate('input.wertiviewinput', 'change', wertiview.phrasalverbs.clozeInputHandler);
		$('body').undelegate('span.wertiviewhint', 'click', wertiview.phrasalverbs.clozeHintHandler);
		
		$('input.wertiviewinput').each( function() {
			$(this).replaceWith($(this).data('wertiviewanswer'));
		});
		$('.wertiviewhint').remove();
	},

	colorize: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		$('span.wertiviewVerb').addClass('colorizeStyleVerb');
		$('span.wertiviewParticle').addClass('colorizeStyleParticle');
	},
	
	colorizeSpan: function(span, topic) {
		span.find('span.wertiviewVerb').addClass('colorizeStyleVerb');
		span.find('span.wertiviewParticle').addClass('colorizeStyleParticle');
	},

	click: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		// change all wertiviewtoken spans to mouseover pointer
		$('span.wertiviewtoken').css({'cursor': 'pointer'});

		// verb markup
		$('span.wertiviewPhrVerb').find('span.wertiviewVerb').addClass('colorizeStyleVerb');

		// handle particle click
		$('body').delegate('span.wertiviewtoken', 'click', {context: contextDoc}, wertiview.phrasalverbs.clickHandler);
	},

	clickHandler: function(event) {
		var contextDoc = event.data.context;

		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		// an already colored verb, leave as is
		var isColored = false;

		if ($(this).hasClass('wertiviewVerb') || $(this).find('.wertiviewVerb').length > 0) {
			isColored = true;
		}

		if (isColored) {
			return false;
		}

		// if this is any other token, particles are correct, other tokens are incorrect
		var isParticle = false;
		var $span = $(this);
		
		// this is a particle
		if ($(this).hasClass('wertiviewParticle') || $(this).find('.wertiviewParticle').length > 0) {
			isParticle = true;
		}
		
		// this is part of a multi-word particle, mark the whole span correct at once
		if ($(this).parents('.wertiviewParticle').length > 0) {
			$span = $(this).parents('.wertiviewParticle').eq(0);
			isParticle = true;
		}
		
		if (isParticle) {
			$span.addClass('clickStyleCorrect');
		} else {
			$span.addClass('clickStyleIncorrect');
		}
		
		$span.css({'cursor': 'auto'});
		
		return false;
	},

	mc: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		// get potential spans
		var $hits = $('span.wertiviewPhrVerb');

		var partList = []; 
		var tokens = [];
		wertiview.phrasalverbs.types = [];
		$hits.each( function() {
			var $hit = $(this);
			// only include if we find both the verb and the particle
			if ($hit.find('.wertiviewVerb').length > 0 && $hit.find('.wertiviewParticle').length > 0) {
				var $part = $hit.find('.wertiviewParticle').eq(0);
				partList.push($part);				
				tokens[$part.text().toLowerCase()] = 1;
			}
		});
		for (word in tokens) {
			wertiview.phrasalverbs.types.push(word);
		}

		wertiview.phrasalverbs.maxLength = wertiview.phrasalverbs.MAX_MC;
		if (wertiview.phrasalverbs.maxLength > wertiview.phrasalverbs.types.length) {
			wertiview.phrasalverbs.maxLength = wertiview.phrasalverbs.types.length;
		}
		
		wertiview.activity.mc(contextDoc, partList, 
				wertiview.phrasalverbs.clozeInputHandler, 
				wertiview.phrasalverbs.clozeHintHandler, 
				wertiview.phrasalverbs.mcGetOptions, 
				wertiview.phrasalverbs.mcGetCorrectAnswer, 
				wertiview.phrasalverbs.mcColorVerb);

	},
	
	mcGetOptions: function($part, capType){
		wertiview.lib.shuffleList(wertiview.phrasalverbs.types);
		var options = [];
		var j = 0;
		while (options.length < wertiview.phrasalverbs.maxLength - 1) {
			if (wertiview.phrasalverbs.types[j] != $part.text().toLowerCase()) {
				options.push(wertiview.lib.matchCapitalization(wertiview.phrasalverbs.types[j], capType));
			}
			j++;
		}
		
		options.push(wertiview.lib.matchCapitalization($part.text(), capType));

		wertiview.lib.shuffleList(options);
		return options;
	},
	
	mcGetCorrectAnswer: function($part, capType){
		return $part.text();
	},
	
	mcColorVerb: function($part, capType){
		var $hit = $part.parent();
		var $verb = $hit.find('.wertiviewVerb').eq(0);
		// colorize the verb
		$verb.addClass('colorizeStyleVerb');
	},

	cloze: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		// get potential spans
		var $hits = $('span.wertiviewPhrVerb');
		
		var partList = []; 
		$hits.each( function() {
			var $hit = $(this);
			// only include if we find both the verb and the particle
			if ($hit.find('.wertiviewVerb').length > 0 && $hit.find('.wertiviewParticle').length > 0) {
				var $part = $hit.find('.wertiviewParticle').eq(0);
				partList.push($part);				
			}
		});
		
		wertiview.activity.cloze(contextDoc, partList, 
				wertiview.phrasalverbs.clozeInputHandler, 
				wertiview.phrasalverbs.clozeHintHandler, 
				wertiview.phrasalverbs.mcGetCorrectAnswer, 
				wertiview.phrasalverbs.mcColorVerb);
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
}); // REMOVE-WITH-MAVEN-REPLACER-PLUGIN
