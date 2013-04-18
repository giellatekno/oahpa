
	wertiview.notification = {
	add: function(notice, contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		var noticeTimeout = 3000; // in ms

		// create divs for popup notice
		var $noticediv = jQuery("<div>");
		$noticediv.attr("id", "wertiview-notification");
		var $messagediv = jQuery("<div>");
		$messagediv.attr("id", "wertiview-notification-message");

		// add message text to div
		$messagediv.text(notice);

		$noticediv.css({'position': 'fixed',
			'bottom': '30px',
			'right': '30px',
			'min-height': '60px',
			'width': '300px',
			'background': '#333333',
			'-moz-border-radius': '5px',
			'border-radius': '5px',
			'border': '1px solid #999999',
			'z-index': '9999',
			'display': 'none'});
		$messagediv.css({'padding': '10px',
			'color': '#eeeeee',
			'display': 'block',
			'font-family': 'sans-serif',
			'font-size': '12pt',
			'position': 'relative',
			'text-align': 'left',
			'display': 'none'});

		$noticediv.append($messagediv);

		// add to page
		$('body').append($noticediv);

		// show/hide message with timeout below
		$('#wertiview-notification').show('600', function() {
			$('#wertiview-notification-message').show('200');
		});
		var timer = Components.classes["@mozilla.org/timer;1"]
					       .createInstance(Components.interfaces.nsITimer);
		var removeNotice = function() {
			$('#wertiview-notification-message').hide('fast');
			$('#wertiview-notification').hide('slow', function() {
				$('#wertiview-notification').remove();
			});
			timer.cancel();
		};
		timer.initWithCallback(removeNotice, noticeTimeout, Components.interfaces.nsITimer.TYPE_ONE_SHOT);
	},

	remove: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		$('#wertiview-notification-message').hide('fast');
		$('#wertiview-notification').hide('fast', function() {
			$('#wertiview-notification').remove();
		});
		
		$('#wertiview-inst-notification').remove();
	},
	
	instDialog: function(notice, contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		var noticeTimeout = 3000; // in ms

		// create divs for popup notice
		var $noticediv = $('<div id="wertiview-inst-notification">');
		var $messagediv = $('<div id="wertiview-inst-message">' + notice + '</div>');
		var $clickdiv = $('<div id="wertiview-inst-click">OK</div>');
		
		var noticeHeight = 80;
		var noticeWidth = 400;

		$noticediv.css({
			'min-height': noticeHeight + 'px',
			'width': noticeWidth + 'px'});
		
		$noticediv.append($messagediv);
		$noticediv.append($clickdiv);

		wertiview.blur.add(contextDoc, false, "0.5");

		// add to page and center
		$('body').append($noticediv);
		$noticediv.css({
			'top': ($('#wertiview-blur').height() - noticeHeight) / 2,
			'left': ($('#wertiview-blur').width() - noticeWidth) / 2
		});

		// show/hide message with timeout below
		$('#wertiview-inst-notification').show(50);
		
		$('body').delegate('#wertiview-inst-notification', 'click', {context: contextDoc}, wertiview.notification.clickToRemove);
	},
	
	clickToRemove: function(event) {
		var jQuery = wertiview.jQuery;
		var contextDoc = event.data.context;
        var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
        $.fn = $.prototype = jQuery.fn;
        
		$(this).hide(0, function() {
			$(this).remove();
		});
		
		wertiview.blur.remove(contextDoc);

		return false;
	},
	
	center: function(elem, contextDoc) {
		var jQuery = wertiview.jQuery;
        var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
        $.fn = $.prototype = jQuery.fn;
        
		return elem.each(function(){
			var element = $(this), win = $(window);
			centerElement();

			jQuery(window).bind('resize',function(){
				centerElement();
			});

			function centerElement(){
				var elementWidth, elementHeight, windowWidth, windowHeight, X2, Y2;
				elementWidth = element.outerWidth();
				elementHeight = element.outerHeight();
				windowWidth = win.width();
				windowHeight = win.height();	
				X2 = (windowWidth/2 - elementWidth/2) + "px";
				Y2 = (windowHeight/2 - elementHeight/2) + "px";
				jQuery(element).css({
					'left':X2,
					'top':Y2,
					'position':'fixed'
				});						
			}
		});
	}
	};

