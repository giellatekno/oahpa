
	// placeholder for HTML content type annotation development
	wertiview.html = {
	
	remove: function(contextDoc) {
	},

	colorize: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		$('span.wertiviewboilerplate').css({'background': 'grey'});
		$('span.wertiviewheadline').css({'background': 'blue'});
		$('span.wertiviewsupplemental').css({'background': 'lime'});
		$('span.wertiviewcontent').css({'background': 'red'});
	},
	
	colorizeSpan: function(span, topic) {
	},

	click: function(contextDoc) {
	},
	
	cloze: function(contextDoc) {
	}
	};
