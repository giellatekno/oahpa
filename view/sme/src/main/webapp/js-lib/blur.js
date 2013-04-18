
	wertiview.blur = {
	add: function(contextDoc, addLoadingImage, opacity) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		if($('wertiview-blur').length == 0) {
			// not using jquery to create overlay to avoid 
			// opacity bug
			var overlay = content.document.createElement("div");
			overlay.id = 'wertiview-blur';
			overlay.style.display = 'block';
			overlay.style.position = 'fixed';
			overlay.style.top = '0';
			overlay.style.left = '0';
			overlay.style.width = '100%';
			overlay.style.height = '100%';
			overlay.style.background = "#ffffff";
			overlay.style.opacity = opacity;
			overlay.style.zIndex = "9998";

			$('body').append(overlay);
			
			if (addLoadingImage) {
				var loadingimg = content.document.createElement("img");
				loadingimg.id = 'wertiview-loading';
				loadingimg.src = "chrome://view/skin/loading.gif";
				loadingimg.width = "32";
				loadingimg.height = "32";
				loadingimg.style.zIndex = "9999";
				loadingimg.style.opacity = "1";
				loadingimg.style.display = 'none';
				loadingimg.style.position = 'fixed';

				$('body').append(loadingimg);
				$('#wertiview-loading').css({
					'top': $('#wertiview-blur').height() / 2 - 16,
					'left': $('#wertiview-blur').width() / 2 - 16
				});
				$('#wertiview-loading').show();
			}
		}
	},

	remove: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		$('#wertiview-loading').remove();
		$('#wertiview-blur').remove();
	}
	};

