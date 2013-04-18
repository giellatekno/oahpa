
	wertiview.lib = {

	getRandom: function(max) {
	    return Math.floor(Math.random() * (max + 1));
	},

	// Fisher-Yates shuffle
	shuffleList: function(elemList) {
		var i, j, tempElem;
		for (i = elemList.length; i > 1; i--) {
			j = parseInt(Math.random() * i);
			tempElem = elemList[j];
			elemList[j] = elemList[i - 1];
			elemList[i - 1] = tempElem;
		}
	},
	
	// Reservoir sampling (sample k elements from an array) applied to 
	// associative arrays, i.e. objects with properties
	// http://en.wikipedia.org/w/index.php?title=Reservoir_sampling&oldid=488484000
	sampleFromObjectProps: function(obj, k) {
		// choose the keys at random
		var sampleKeys = {};
		var i = 0;
		for (var key in obj) {
			// generate the reservoir
			if (i < k){
				sampleKeys[i] = key;
			}
			else {
				// randomly replace elements in the reservoir with a decreasing probability
				var r = wertiview.lib.getRandom(i+1);
				if (r < k) {
					sampleKeys[r] = key;
				}
			}
			i++;
		}
		// find the corresponding values for the chosen keys
		var sample = {};
		for (var j=0; j<k; j++){
			key = sampleKeys[j];
			var value = obj[key];
			sample[key] = value;
		}
		return sample;
	},
	
	// handler for disabling click on <a> elements in click activities
	clickDisableLink: function() {
		return false;
	},
	
	// handler for disabling click/submit within <a> elements in cloze activities
	clozeDisableLink: function(event) {
		var contextDoc = event.data.context;

		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		// if there is an input box in the link, disable
		if ($(this).find('.wertiviewinput').length > 0) {
			return false;
		}

		// if the input box was just removed, remove flag and only disable for this click
		if ($(this).data('wertiview-disableclick')) {
			$(this).removeData('wertiview-disableclick');
			return false;
		}

		// enable link
		return true;
	},

	replaceInput: function($old, $new) {
		// if this is inside a link
		if ($old.parents('a').length > 0) {
			$old.parents('a').eq(0).data('wertiview-disableclick', true);	
		}

		$old.replaceWith($new);
	},
	
	// detect capitalization pattern in target word
	// 0 = not capitalized or weird enough to leave alone
	// 1 = all caps
	// 2 = first letter capitalized
	detectCapitalization: function(word) {
		type = 0;
		if (word == word.toUpperCase()) {
			type = 1;
		} else if (word == word.substr(0, 1).toUpperCase() + word.substr(1)) {
			type = 2;
		}
		return type;
	},
	
	// parallel capitalization (for multiple choice drop-downs)
	matchCapitalization: function(word, type) {
		switch(type) {
		case 0:
			return word;
		case 1:
			return word.toUpperCase();
		case 2:
			return word.slice(0, 1).toUpperCase() + word.slice(1);
		default:
			return word;
		}
	},
	
	encodeUTF8: function(s) {
	  return unescape(encodeURIComponent(s));
	},

	decodeUTF8: function (s) {
	  return decodeURIComponent(escape(s));
	},
	
	inExtension: function() {
		var activity = window['wertiview']['load'];

		// if this function exists, this is the extension
		if(activity != undefined) {
			return true;
		}
		
		// otherwise, this is the web interface
		return false;
	},
	
	doNothing: function(){},
	
	// TODO remove before reintegrating
	obj2str: function(obj, recursive) {
		if (recursive == undefined) {
			recursive = false;
		}
		
		if (typeof obj != 'object') {
			return "" + obj;
		}
		
		var MAX_STR_LEN = 30;
		var str = "{";
		for (var key in obj) {
			var val = obj[key];
			if (typeof val == 'function') {
				//str += key + ": function\n";
			}
			else if (typeof val == typeof "") {
				if (val.length > MAX_STR_LEN) {
					part = "'" +  val.substring(0, MAX_STR_LEN) + "…' (" + val.length + ")";
				}
				else {
					part = "'" + val + "'";
				}
				str += key + ": " + part + "\n";
			}
			else if (val != undefined && val != null) {
				if (recursive) {
					val = wertiview.lib.obj2str(val, recursive);
				}
				str += key + ": " + val + "\n";
			}
		}
		return str + "}";
	}
	
	};

