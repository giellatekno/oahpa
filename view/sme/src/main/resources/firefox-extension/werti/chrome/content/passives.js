wertiview.ns(function() {
	wertiview.passives = {
			
	MAX_CLOZE: 20,
	
	remove: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		// remove cloze
		$('.wertiviewPassive').each( function() {
			if ($(this).find('.wertiviewinput').length > 0) {
				$(this).empty();
				$(this).html($(this).data('wertiview-original-text'));
			}
		});
		
		// temporary, while colorize inserts sentence
		//$('.clozeStylePassiveConversion').remove();
		$('.wertiviewPassive').remove();

		$('body').undelegate('span.wertiviewcheck', 'click', wertiview.passives.clozeCheckHandler);
		$('body').undelegate('span.wertiviewclear', 'click', wertiview.passives.clozeClearHandler);
		$('body').undelegate('span.wertiviewhint', 'click', wertiview.passives.clozeHintHandler);
		$('body').undelegate('input.wertiviewinput', 'keyup keydown blur', wertiview.passives.clozeWidthHandler);
	},

	colorize: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		$('span.wertiviewPassive').each( function () {
			$(this).addClass('colorizeStylePassive');
		});
	},
	
	colorizeSpan: function(span, topic) {
		span.find('span.wertiviewPassive').addClass('colorizeStylePassive');
	},
	
	/* click: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		$('span.wertiviewPassive').each( function () {
			var $span = $('<span>');
			$span.addClass('clozeStylePassiveConversion');
			$span.text(' (' + $(this).attr('title') + ') ');
			$(this).append($span);
		});
	},
	
	cloze: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		$('span.wertiviewPassive').each( function () {
			$(this).data('wertiview-original-text', $(this).html());
			$(this).data('wertiview-target-text', $(this).text());
			
			// if this contains links, skip
			if ($(this).find('a').length > 0) {
				return;
			}
			
			$(this).html('');

			// create input field
			var $input = $('<input>');
			$input.attr('type', 'text');
			$input.attr('id', $(this).attr('id') + '-input');
			$input.addClass('clozeStyleInputAdjust');
			$input.addClass('clozeStyleInputUnknown');
			$input.addClass('wertiviewinput');
			$(this).append($input);
			
			// create check button
			var $check = $('<span>');
			$check.attr('id', $(this).attr('id') + '-check');
			$check.addClass('clozeStyleHint');
			$check.html("&#10003;");
			$check.addClass('wertiviewcheck');
			$(this).append($check);
			
			// create clear button
			var $clear = $('<span>');
			$clear.attr('id', $(this).attr('id') + '-clear');
			$clear.addClass('clozeStyleHint');
			$clear.html("&#10007;");
			$clear.addClass('wertiviewclear');
			$(this).append($clear);

			// create hint ? button
			var $hint = $('<span>');
			$hint.attr('id', $(this).attr('id') + '-hint');
			$hint.addClass('clozeStyleHint');
			$hint.text("?");
			$hint.addClass('wertiviewhint');
			$(this).append($hint);
			
			// insert sentence
			var $orig = $('<span>');
			$orig.attr('id', $(this).attr('id') + '-conversion');
			$orig.addClass('clozeStylePassiveConversion');
			$orig.text(' (' + $(this).attr('title') + ') ');
			$(this).append($orig);
		});
		
		$('body').delegate('span.wertiviewcheck', 'click', {context: contextDoc}, wertiview.passives.clozeCheckHandler);
		$('body').delegate('span.wertiviewclear', 'click', {context: contextDoc}, wertiview.passives.clozeClearHandler);
		$('body').delegate('span.wertiviewhint', 'click', {context: contextDoc}, wertiview.passives.clozeHintHandler);
		$('body').delegate('input.wertiviewinput', 'keyup keydown blur', {context: contextDoc}, wertiview.passives.clozeWidthHandler);
	},
	
	clozeCheckHandler: function(event) {
		var contextDoc = event.data.context;
		
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		var $qParent = $(this).parents('.wertiviewPassive').eq(0);
		var $input = $qParent.find('.wertiviewinput').eq(0);
	
		var currentText = $input.val();
		var targetText = $qParent.data('wertiview-target-text');

		currentText = wertiview.passives.compareFormat(currentText);
		targetText = wertiview.passives.compareFormat(targetText);
		
		if (currentText == targetText) {
			$qParent.empty();
			$qParent.html($qParent.data('wertiview-original-text'));
			$qParent.addClass('clozeStyleCorrect');
		} else {
			$input.removeClass('clozeStyleInputUnknown');
			$input.addClass('clozeStyleInputIncorrect');
		}
		
		return false;
	},
	
	clozeHintHandler: function(event) {
		var jQuery = wertiview.jQuery;
		var contextDoc = event.data.context;
		  var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		  $.fn = $.prototype = jQuery.fn;

		var nextInput;

		// fill in the answer by replacing input with text
		$text = $('<span>');
		$text.addClass('clozeStyleProvided');
		$text.text($(this).parent().data('wertiview-target-text'));
		wertiview.lib.replaceInput($(this).parent(), $text);
		
		return false;
	},
	
	clozeClearHandler: function(event) {
		var contextDoc = event.data.context;
		
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		var $qParent = $(this).parents('.wertiviewPassive').eq(0);
		var $input = $qParent.find('.wertiviewinput').eq(0);
		
		$input.val('');
		$input.removeClass('clozeStyleInputIncorrect');
		$input.addClass('clozeStyleInputUnknown');
		
		$input.trigger('keyup');
		
		return false;
	},
	
	clozeWidthHandler: function(event) {
		var contextDoc = event.data.context;

		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		var minWidth = 50;
		var maxWidth = 500;
		var extraWidth = 20;
		
		var oldWidth = $(this).width();
		
		$hiddenDiv = $('<div/>').css({'position': 'absolute',
			  'top': '0',
			  'left': '0',
			  'visibility': 'hidden',
			  'fontSize': $(this).css('fontSize'),
			  'fontFamily': $(this).css('fontFamily'),
			  'fontWeight': $(this).css('fontWeight'),
			  'letterSpacing': $(this).css('letterSpacing'),
			  'whiteSpace': 'nowrap'});
		
		$hiddenDiv.text($(this).val());
		$hiddenDiv.insertAfter($(this));
		var hiddenWidth = $hiddenDiv.width();
		$hiddenDiv.remove();
		
		var newWidth = hiddenWidth;
		
		if (hiddenWidth < minWidth) {
			newWidth = minWidth;
		}
		
		if (hiddenWidth > maxWidth) {
			newWidth = maxWidth;
		}
		
		newWidth += extraWidth;
		
		$(this).width(newWidth);
	}, */

	compareFormat: function(text) {
		return text.toLowerCase().replace(/[^\w]/g, '');
	}
	};
}); // REMOVE-WITH-MAVEN-REPLACER-PLUGIN
