wertiview.ns(function() {
	wertiview.activity = {

	// add wertiview markup
	add: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		// identify context document under consideration
		contextDoc = contextDoc||window.content.document;

		// disable toolbar button
		wertiview.toolbar.disableRunButton();

		// load options from preferences
		var options = wertiview.getOptions();

		// remove any previous activity from this page
		if ($('.wertiview').length > 0) {
			wertiview.activity.remove(contextDoc);
		}
		
		// check for appropriate selections
		if (options['language'] == "unselected") {
			alert("Please select a language!");
			wertiview.toolbar.enableRunButton();
			return;
		} else if (options['topic'] == "unselected") {
			alert("Please select a topic!");
			wertiview.toolbar.enableRunButton();
			return;
		} else if (options['activity'] == "unselected") {
			alert("Please select an activity!");
			wertiview.toolbar.enableRunButton();
			return;
		}
		
		var topicName = wertiview.activity.getTopicName(options['topic']);
		
		// check whether this topic/activity exists as a function
		if (!window['wertiview'][topicName] || !window['wertiview'][topicName][options['activity']]) {
			alert("The selected topic and activity are not available.");
			wertiview.toolbar.enableRunButton();
			return;
		}
		
		var activityFunction = window['wertiview'][topicName][options['activity']];

		if(typeof activityFunction !== 'function') {
			alert("The selected topic and activity are not available.");
			wertiview.toolbar.enableRunButton();
			return;
		}

		// blur the page for cloze activity
		if (options['activity'] == "cloze") {
			wertiview.blur.add(contextDoc, true, "0.9");
		}

		// save the options used in the page
		$('body').data('wertiview-language', options['language']);
		$('body').data('wertiview-topic', options['topic']);
		$('body').data('wertiview-activity', options['activity']);

		// add the markup
		var counter = 1;

		var contextDocCopy = contextDoc.cloneNode(true);

		var textNodes = wertiview.activity.getTextNodesIn(contextDoc.body);
		var textNodesCopy = wertiview.activity.getTextNodesIn(contextDocCopy.body);
		
		$(textNodes).each( function() {
			var thisCopy = textNodesCopy[counter-1];
			// store span id internally
			$(this).data('wertiview', counter);
			$(thisCopy).data('wertiview', counter);

			// make hidden text-node ids visible by wrapping <span>s around them
			$(thisCopy).wrap( function () {
				return '<span class="wertiview" wertiviewid="' + counter + '"></span>';
			});

			counter += 1;
		});
		
		
		wertiview.activity.sendAjaxRequest(contextDocCopy, options, contextDoc);
	},
	
	sendAjaxRequest: function(contextDocCopy, options, contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,context||contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		// if spans are found, send to server
		if ($('span.wertiview', contextDocCopy).length > 0) {
			var activityData = {};
			activityData['type'] = "page";
			activityData['url'] = wertiview.getURL(contextDocCopy);
			activityData['language'] = options['language'];
			activityData['topic'] = options['topic'];
			activityData['activity'] = options['activity'];
			activityData['document'] = contextDocCopy.documentElement.outerHTML;
			activityData['version'] = wertiview.VERSION;

			jQuery.ajax({
				type: "POST",
				url: wertiview.servletURL,
				data: wertiview.nativeJSON.encode(activityData),
				processData: false,
				timeout: 60000,
				success: function(data, textStatus, xhr) { 
					if (data) {
						wertiview.activity.addServerMarkup(data, options, contextDoc); 
					} else {
						wertiview.activity.ajaxError(xhr, "nodata");
						wertiview.toolbar.enableRunButton();
					}
				},
				error: wertiview.activity.ajaxError
			});
		} else {
			wertiview.blur.remove(contextDoc);
			wertiview.toolbar.enableRunButton();
		}
	},

	// add the markup sent from the servlet to the page
	addServerMarkup: function(data, options, contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		// parse result from wertiview servlet from JSON into list
		var dataList = wertiview.nativeJSON.decode(data);
		
		// identify context document under consideration
		contextDoc = contextDoc||window.content.document;

		var counter = 0;
		var newcontent;
		var spans = [];
		
		var textNodes = wertiview.activity.getTextNodesIn(contextDoc.body);
		
		$(textNodes).each( function() {
			if ($(this).data('wertiview')) {
				spans.push($(this));
			}
		});

		var length = spans.length;
		var index = 0;
		var span;
		var timer = Components.classes["@mozilla.org/timer;1"]
					       .createInstance(Components.interfaces.nsITimer);
		
		var addwertiviewspans = function() {
			while (spans.length > 0) {
				span = spans.shift();
				counter = span.data('wertiview');

				// retrieve matching updated content
				newcontent = dataList[counter];
				if(newcontent != null) {
					newspan = $(newcontent);

					// colorize before adding spans
					if (options['activity'] == 'colorize') {
						var topicName = wertiview.activity.getTopicName(options['topic']);

						// check whether this topic/activity exists as a function
						var colorizeFunction = window['wertiview'][topicName]['colorizeSpan'];

						if(typeof colorizeFunction === 'function') {
							colorizeFunction(newspan, options['topic']);
						}
					}

					// replace old content with new content
					span.replaceWith(newspan);
				}
				
				// Firefox needs a break after every 50 changes
				if (counter % 50 == 0) {
					return;
				}
			}

			wertiview.activity.addActivity(options, contextDoc);
			wertiview.toolbar.enableRunButton();
			wertiview.toolbar.enableRestoreButton();
			
			timer.cancel();
		};
		
		timer.initWithCallback(addwertiviewspans, 5, Components.interfaces.nsITimer.TYPE_REPEATING_SLACK);
		// note that anything after this point will probably
		// happen BEFORE the addwertiviewspans/timer loop finishes!
	},

	// add JS/etc. for activity
	addActivity: function(options, contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		var topicName = wertiview.activity.getTopicName(options['topic']);
		var activityFunction = window['wertiview'][topicName][options['activity']];

		switch(options['activity']) {
			case 'colorize':
				wertiview.notification.add("VIEW Colorize Activity Ready", contextDoc);
				break;
			case 'click':
				// remove click from all links
				$('body').delegate('a', 'click', wertiview.lib.clickDisableLink);

				activityFunction(contextDoc);
				wertiview.notification.add("VIEW Click Activity Ready", contextDoc);
				break;
			case 'mc':
				// no link disabling because the drop-down boxes are prevented
				// from showing up with links because they act strange in links

				activityFunction(contextDoc);
				wertiview.notification.add("VIEW Multiple Choice Activity Ready", contextDoc);
				break;
			case 'cloze':
				// remove click from all links that contain input boxes
				$('body').delegate('a', 'click', {context: contextDoc}, wertiview.lib.clozeDisableLink);
				
				activityFunction(contextDoc);
				wertiview.notification.add("VIEW Practice Activity Ready", contextDoc);
				wertiview.blur.remove(contextDoc);
				break;
			default:
				wertiview.blur.remove(contextDoc);
				// we should never get here
				alert('Invalid activity');
		}
	},

	// remove wertiview markup
	remove: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		// identify context document under consideration
		contextDoc = contextDoc||window.content.document;

		var savedOptions = {};
		savedOptions['language'] = $('body').data('wertiview-language');
		savedOptions['topic'] = $('body').data('wertiview-topic');
		savedOptions['activity'] = $('body').data('wertiview-activity');
		$('body').removeData('wertiview-language');
		$('body').removeData('wertiview-topic');
		$('body').removeData('wertiview-activity');
		
		var topicName = wertiview.activity.getTopicName(savedOptions['topic']);
		
		// if we can't find a topic name, skip the rest of the removal
		if (topicName == null) {
			return;
		}

		// generate remove function for this topic and make sure
		// the function exists before calling
		var removeFunction = window['wertiview'][topicName]['remove'];
		
		if(typeof removeFunction !== 'function') {
			alert("Error removing activity.  Please reload the page.");
			return;
		}
		
		removeFunction(contextDoc);

		$('.wertiview').each( function() {
			$(this).replaceWith($(this).text());
		});

		$('body').undelegate('a', 'click', wertiview.lib.clickDisableLink);
		$('body').undelegate('a', 'click keydown', wertiview.lib.clozeDisableLink);
		wertiview.toolbar.disableRestoreButton();
		wertiview.notification.remove(contextDoc);
		wertiview.blur.remove(contextDoc);
	},
	
	getTopicName: function(topic) {
		if (topic == null) {
			return null;
		}
		
		// figure out corresponding topic name
		var topicName = topic.toLowerCase();

		// exceptions: 
		//   - Arts and Dets and Preps use the 'pos' topic
		switch(topic) {
			case "Arts":
			case "Dets":
			case "Preps":
				topicName = 'pos';
				break;
			default:
				break; 
		}
		
		return topicName;
	},

	ajaxError: function(xhr, textStatus, errorThrown) {       
		wertiview.toolbar.enableRunButton();
		wertiview.blur.remove();

		if (!xhr || !textStatus) {
			alert("The VIEW server encountered an error.");
			return;
		}

		switch(textStatus) {
			case "nodata":
				alert("The VIEW server is currently unavailable.");
				break;
			case "timeout":
				alert("The VIEW server is taking too long to respond.");
				break;
			case "error":
				switch (xhr.status) {
					case 490:
						alert("The VIEW server no longer supports this version of the VIEW extension.\nPlease check for a new version of the add-on in the Tools->Add-ons menu!");
						break;
					case 491:
						alert("The topic selected isn't available.\nPlease select a different topic from the toolbar menu.");
						break;
					case 492:
						alert("The topic selected isn't available for the language selected.\nPlease select a different language or topic from the toolbar menu.");
						break;
					default:
						alert("The VIEW server encountered an error.");
						break;
				}
				break;
			default:
				alert("The VIEW server encountered an error.");
				break;
		}
	},
	
	// adapted from: http://stackoverflow.com/questions/298750/how-do-i-select-text-nodes-with-jquery
	getTextNodesIn: function(node) {
	    var textNodes = [];

	    function getTextNodes(node) {
	        if (node.nodeType == 3 && (/[^\t\n\r ]/.test(node.nodeValue))) {
	            textNodes.push(node);
	        } else if (node.nodeName == "SCRIPT" || node.nodeName == "NOSCRIPT" || node.nodeName == "STYLE") {
	        	// skip this node
	        } else {
	            for (var i = 0, len = node.childNodes.length; i < len; ++i) {
	                getTextNodes(node.childNodes[i]);
	            }
	        }
	    }

	    getTextNodes(node);
	    return textNodes;
	},
	
	// generate multiple choice exercises
	// @param hitList list of hits that could be turned into exercises, unwanted instance must be removed in advance
	// @param getOptionsCallback a function that returns an array of choices to be presented to the user
	// @param getCorrectAnswerCallback a function that returns the correct answer choice for a given hit
	// @param addProcCallback a function that is called for every exercise (default: wertiview.lib.doNothing)
	// @param emptyHit if true, the hit text will be erased (default: true)
	// @param partExercises decimal by which the number of exercises to generate is multiplied in 'fixed number' mode (default: 1.0)
	mc: function(contextDoc, hitList, inputHandler, hintHandler, 
			getOptionsCallback, getCorrectAnswerCallback, addProcCallback, 
			emptyHit, partExercises){
		
		if (typeof addProcCallback == 'undefined'){
			addProcCallback = wertiview.lib.doNothing;
		}
		if (typeof emptyHit == 'undefined'){
			emptyHit = true;
		}
		if (typeof partExercises == 'undefined'){
			partExercises = 1.0;
		}

		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
        $.fn = $.prototype = jQuery.fn;
		
    	// calculate the number of hits to turn into exercises
        var numExercises = 0;
        var fixedOrPercentage = wertiview.getFixedOrPercentage();
        if (fixedOrPercentage == wertiview.pref_fixedNumber) {
            numExercises = wertiview.getFixedNumberOfExercises() * partExercises;
        }
        else if (fixedOrPercentage == wertiview.pref_percentage) {
        	numExercises = wertiview.getProportionOfExercisesDec() * hitList.length;
        }
        else {
        	// we should never get here
        	wertiview.prefError();
        }
        if (hitList.length < 20) {
            numExercises = hitList.length - 2;
        }
        //alert("nr of exercises: "+numExercises);
        
        // choose which hits to turn into exercises
        var i = 0;
        var inc = 1;
        var choiceMode = wertiview.getChoiceMode();
        if (choiceMode == wertiview.pref_random) {
            wertiview.lib.shuffleList(hitList);
        }
        else if (choiceMode == wertiview.pref_first) {
        	i = wertiview.getFirstOffset();
        }
        else if (choiceMode == wertiview.pref_intervals){
        	inc = wertiview.getIntervalSize();
        }
        else {
        	// we should never get here
        	wertiview.prefError();
        }
        
        // generate the exercises
        //alert("generating exercises");
        for (; numExercises > 0 && i < hitList.length; i += inc){
        	var $hit = hitList[i];
        	//alert("next hit: "+$hit);

        	// if the span is inside a link, skip (drop-down boxes are weirder 
    		// than text input boxes, need to investigate further)
    		if ($hit.parents('a').length > 0) {
                //alert("this is inside a link");
    			continue;
    		}

    		var capType = wertiview.lib.detectCapitalization($hit.text());
        	
    		// choices for the user
        	var options = getOptionsCallback($hit, capType);
        	//alert("answer variants: "+options);
        	// correct choice
        	var answer = getCorrectAnswerCallback($hit, capType);
        	//alert("correct answer: "+answer);
        	
        	// e.g., phrasalverbs needs to add colorization to the verb
        	addProcCallback($hit, capType);

    		// create select box
    		var $input = $('<select>');
    		$input.attr('style','width: auto');
    		var inputId = $hit.attr('id') + '-select';
    		$input.attr('id', inputId);
    		$input.addClass('wertiviewinput');
    		var $option = $('<option>');
    		$option.html(" ");
    		$input.append($option);
    		for (var j = 0; j < options.length; j++) {
    			$option = $('<option>');
    			$option.text(options[j]);
    			$input.append($option);
    		}
    		$input.data('wertivieworiginaltext', $hit.text());
    		$input.data('wertiviewanswer', answer);
    		if (emptyHit){
    			$hit.empty();
    		}
    		$hit.append($input);
    		
    		// create hint ? button
    		var $hint = $('<span>');
    		$hint.attr('id', $hit.attr('id') + '-hint');
    		$hint.addClass('clozeStyleHint');
    		$hint.text("?");
    		$hint.addClass('wertiviewhint');
    		$hit.append($hint);

    		// count down numExercises until we're finished
			numExercises--;
        }

        $('body').delegate('select.wertiviewinput', 'change', {context: contextDoc}, inputHandler);
		$('body').delegate('span.wertiviewhint', 'click', {context: contextDoc}, hintHandler);
	},

	// generate practice exercises
	// @param hitList list of hits that could be turned into exercises, unwanted instance must be removed in advance
	// @param getCorrectAnswerCallback a function that returns the correct answer choice for a given hit
	// @param addProcCallback a function that is called for every exercise (default: wertiview.lib.doNothing)
	// @param emptyHit if true, the hit text will be erased (default: true)
	// @param partExercises decimal by which the number of exercises to generate is multiplied in 'fixed number' mode (default: 1.0)
	cloze: function(contextDoc, hitList, inputHandler, hintHandler, 
			getCorrectAnswerCallback, addProcCallback, 
			emptyHit, partExercises){
		
		if (typeof addProcCallback == 'undefined'){
			addProcCallback = wertiview.lib.doNothing;
		}
		if (typeof emptyHit == 'undefined'){
			emptyHit = true;
		}
		if (typeof partExercises == 'undefined'){
			partExercises = 1.0;
		}

		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
        $.fn = $.prototype = jQuery.fn;

    	// calculate the number of hits to turn into exercises
        var numExercises = 0;
        var fixedOrPercentage = wertiview.getFixedOrPercentage();
        if (fixedOrPercentage == wertiview.pref_fixedNumber) {
            numExercises = wertiview.getFixedNumberOfExercises() * partExercises;
        }
        else if (fixedOrPercentage == wertiview.pref_percentage) {
        	numExercises = wertiview.getProportionOfExercisesDec() * hitList.length;
        }
        else {
        	// we should never get here
        	wertiview.prefError();
        }
        
        // choose which hits to turn into exercises
        var i = 0;
        var inc = 1;
        var choiceMode = wertiview.getChoiceMode();
        if (choiceMode == wertiview.pref_random) {
            wertiview.lib.shuffleList(hitList);
        }
        else if (choiceMode == wertiview.pref_first) {
        	i = wertiview.getFirstOffset();
        }
        else if (choiceMode == wertiview.pref_intervals){
        	inc = wertiview.getIntervalSize();
        }
        else {
        	// we should never get here
        	wertiview.prefError();
        }
        
        // generate the exercises
        for (; numExercises > 0 && i < hitList.length; i += inc){
			var $hit = hitList[i];
			
    		var capType = wertiview.lib.detectCapitalization($hit.text());
        	
        	// correct choice
        	var answer = getCorrectAnswerCallback($hit, capType);

			// create input box
			var $input = $('<input>');
			$input.attr('type', 'text');
			$input.attr('id', $hit.attr('id') + '-input');
			$input.addClass('clozeStyleInput');
			$input.addClass('wertiviewinput');
			$input.data('wertiviewanswer', answer);
			if (emptyHit) {
				$hit.empty();
			}
			$hit.append($input);
			
			// create hint ? button
			var $hint = $('<span>');
			$hint.attr('id', $hit.attr('id') + '-hint');
			$hint.addClass('clozeStyleHint');
			$hint.text("?");
			$hint.addClass('wertiviewhint');
			$hit.append($hint);
        	
        	// e.g., phrasalverbs needs to add colorization to the verb
			// and gerunds needs to display the base form
        	addProcCallback($hit, capType, $);

    		// count down numExercises until we're finished
			numExercises--;
		}
		
		// figure out next field
		var prevhit = null;
		var nexthits = {};
	
		$('input.wertiviewinput').each( function() {
			// keep track of links to next input field
			if (prevhit) {
				nexthits[prevhit] = $(this).attr('id');
			}
			prevhit = $(this).attr('id');
		});
		
		// add the next input info to each input field
		$('input.wertiviewinput').each( function() {
			if (nexthits[$(this).attr('id')]) {
				$(this).data('wertiviewnexthit', nexthits[$(this).attr('id')]);
			} else {
				$(this).data('wertiviewnexthit', null);
			}
		});

		$('body').delegate('input.wertiviewinput', 'change', {context: contextDoc}, inputHandler);
		$('body').delegate('span.wertiviewhint', 'click', {context: contextDoc}, hintHandler);
	}
	
	};
}); // REMOVE-WITH-MAVEN-REPLACER-PLUGIN
