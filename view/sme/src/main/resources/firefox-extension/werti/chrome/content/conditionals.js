wertiview.ns(function() {
	wertiview.conditionals = {
	remove: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		$('body').undelegate('span.wertiviewtoken', 'click', wertiview.conditionals.clickHandler);
	},

	colorize: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		$('span.wertiviewhit').css({'color': 'green'});
	},

	click: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		// change all wertiviewcs spans to mouseover pointer
		$('span.wertiviewcs').css({'cursor': 'pointer'});

		// handle conditional sentence clicking
		$('body').delegate('span.wertiviewcs', 'click', {context: contextDoc}, wertiview.conditionals.clickHandler);
	},

	clickHandler: function(event) {
		var contextDoc = event.data.context;

		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		if($(this).hasClass('wertiviewhit')) {
			$(this).css({'color': 'green', 'cursor': 'text'});
		} else {
			$(this).css({'color': 'red', 'cursor': 'text'});
		}
		return false;
	}
	};
});
