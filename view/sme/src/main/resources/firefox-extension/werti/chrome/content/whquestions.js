wertiview.ns(function() {
	wertiview.whquestions = {

	relevantChunks: {'wertiviewAUX': 'aux/modal verb',
			  'wertiviewSUBJ': 'subject',
			  'wertiviewNFIN': 'non-finite verb',
			  'wertiviewMVERB': 'main finite verb',
			  'wertiviewWHS': 'wh-subject',
			  'wertiviewWH': 'wh-phrase'},
	
	remove: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		// remove click
		$('body').undelegate('span.wertiviewchunk', 'click', wertiview.whquestions.clickChunkHandler);
		$('body').undelegate('span.wertiviewtoken', 'click', wertiview.whquestions.clickTokenHandler);
		$('span.wertiviewtargetinfo').remove();
		
		// remove cloze
		$('.wertiviewQ').each( function() {
			if ($(this).find('.wertiviewinput').length > 0) {
				$(this).empty();
				$(this).html($(this).data('wertiview-original-text'));
			}
		});

		$('body').undelegate('span.wertiviewQ span.wertiviewchunk', 'click', wertiview.whquestions.clozeSpanHandler);
		$('body').undelegate('span.wertiviewQ span.wertiviewtoken', 'click', wertiview.whquestions.clozeSpanHandler);
		$('body').undelegate('span.wertiviewQ span.wertiviewrestofq', 'click', wertiview.whquestions.clozeSpanHandler);
		$('body').undelegate('span.wertiviewcheck', 'click', wertiview.whquestions.clozeCheckHandler);
		$('body').undelegate('span.wertiviewclear', 'click', wertiview.whquestions.clozeClearHandler);
		$('body').undelegate('span.wertiviewhint', 'click', wertiview.whquestions.clozeHintHandler);
		$('body').undelegate('input.wertiviewinput', 'keyup keydown blur', wertiview.whquestions.clozeWidthHandler);
	},

	colorize: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		$('span.wertiviewWHS').addClass('colorizeStyleWHS');
		$('span.wertiviewWH').addClass('colorizeStyleWH');
		$('span.wertiviewSUBJ').addClass('colorizeStyleSUBJ');
		$('span.wertiviewMVERB').addClass('colorizeStyleMVERB');
		$('span.wertiviewNFIN').addClass('colorizeStyleNFIN');
		$('span.wertiviewAUX').addClass('colorizeStyleAUX');
	},
	
	colorizeSpan: function(span, topic) {
		span.find('span.wertiviewWHS').addClass('colorizeStyleWHS');
		span.find('span.wertiviewWH').addClass('colorizeStyleWH');
		span.find('span.wertiviewSUBJ').addClass('colorizeStyleSUBJ');
		span.find('span.wertiviewMVERB').addClass('colorizeStyleMVERB');
		span.find('span.wertiviewNFIN').addClass('colorizeStyleNFIN');
		span.find('span.wertiviewAUX').addClass('colorizeStyleAUX');
	},

	click: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
	
		// initially mark all chunks as not targets
		$('span.wertiviewchunk').data('wertiview-whquestion-target', false);
		
		var findTargets = Array();
		for (className in wertiview.whquestions.relevantChunks) {
			findTargets.push('span.' + className);
		}
		var findTargetsString = findTargets.join(',');
		
		$('span.wertiviewQ').each( function () {
			var $targets = $(this).find(findTargetsString);
			var $target = $targets.eq(wertiview.lib.getRandom($targets.length - 1));
			// set random target to true
			$target.data('wertiview-whquestion-target', true);
			
			// add category to end of question
			var $targetspan = $('<span>');
			
			var clickStyleTarget = 'clickStyleWH';
			if ($target.hasClass('wertiviewWHS')) {
				clickStyleTarget = 'clickStyleWHS';
			} else if ($target.hasClass('wertiviewWH')) {
				clickStyleTarget = 'clickStyleWH';
			} else if ($target.hasClass('wertiviewSUBJ')) {
				clickStyleTarget = 'clickStyleSUBJ';
			} else if ($target.hasClass('wertiviewMVERB')) {
				clickStyleTarget = 'clickStyleMVERB';
			} else if ($target.hasClass('wertiviewNFIN')) {
				clickStyleTarget = 'clickStyleNFIN';
			} else if ($target.hasClass('wertiviewAUX')) {
				clickStyleTarget = 'clickStyleAUX';
			}
			
			$targetspan.addClass(clickStyleTarget);
			$targetspan.addClass('wertiview');
			$targetspan.addClass('wertiviewtargetinfo');
			
			var numTargets = 0;
			var targetInfo;
			for (className in wertiview.whquestions.relevantChunks) {
				if($target.hasClass(className)) {
					numTargets = $(this).find('.' + className).length;
					targetInfo = wertiview.whquestions.relevantChunks[className];
				}
			}

			// add target info to end of span
			if (targetInfo) {
				$targetspan.text(targetInfo);
			}
			
			// if there's just one of the target, make a click activity
			if (numTargets == 1) {
				// change all wertiviewtoken and wertiviewchunk spans within this question to mouseover pointer
				$(this).find('span.wertiviewtoken').css({'cursor': 'pointer'});
				$(this).find('span.wertiviewchunk').css({'cursor': 'pointer'});

				// add the info about what to click
				$(this).append(' ');
				$(this).append($targetspan);
			}
		});
		
		// handle click
		$('body').delegate('span.wertiviewchunk', 'click', {context: contextDoc}, wertiview.whquestions.clickChunkHandler);
		$('body').delegate('span.wertiviewtoken', 'click', {context: contextDoc}, wertiview.whquestions.clickTokenHandler);
	},

	clickChunkHandler: function(event) {
		var contextDoc = event.data.context;

		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		// ignore the wider wertiviewchunk spans
		if (!($(this).hasClass('wertiviewAUX') || $(this).hasClass('wertiviewSUBJ') || $(this).hasClass('wertiviewNFIN') || 
				$(this).hasClass('wertiviewMVERB') || $(this).hasClass('wertiviewWHS') || $(this).hasClass('wertiviewWH'))) {
			return false;
		}

		if ($(this).parents('.wertiviewQ').length > 0) {
			if ($(this).data('wertiview-whquestion-target')) {
				$(this).addClass('clickStyleCorrect');
			} else {
				$(this).addClass('clickStyleIncorrect');
			}
			$(this).css({'cursor': 'auto'});
		}
		
		return false;
	},
	
	clickTokenHandler: function(event) {
		var contextDoc = event.data.context;

		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		// not within a question
		if ($(this).parents('.wertiviewQ').length == 0) {
			return false;
		}
		
		// non-marked up word within a question
		if ($(this).parents('.wertiviewQ').length > 0 && 
				$(this).parents('.wertiviewAUX,.wertiviewSUBJ,.wertiviewNFIN,.wertiviewMVERB,.wertiviewWHS,.wertiviewWH').length == 0 && 
				$(this).children('.wertiviewAUX,.wertiviewSUBJ,.wertiviewNFIN,.wertiviewMVERB,.wertiviewWHS,.wertiviewWH').length == 0) {
			$(this).addClass('clickStyleIncorrect');
			$(this).css({'cursor': 'auto'});

			// color and stop event propogation
			return false;
		}
		
		// allow event to propogate up to the wertiviewchunk level
		return true;
	},
	
	cloze: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		var findTargets = Array();
		for (className in wertiview.whquestions.relevantChunks) {
			findTargets.push('span.' + className);
		}
		var findTargetsString = findTargets.join(',');
		
		var $hits = $('span.wertiviewQ');

		// calculate the number of hits to turn into exercises
        var numExercises = 0;
        var fixedOrPercentage = wertiview.getFixedOrPercentage();
        if (fixedOrPercentage == wertiview.pref_fixedNumber) {
            numExercises = wertiview.getFixedNumberOfExercises();
        }
        else if (fixedOrPercentage == wertiview.pref_percentage) {
        	numExercises = wertiview.getProportionOfExercisesDec() * $hits.length;
        }
        else {
        	// we should never get here
        	wertiview.ajaxError();
        }
        
        // choose which hits to turn into exercises
        var offset = 0;
        var step = 1;
        var choiceMode = wertiview.getChoiceMode();
        if (choiceMode == wertiview.pref_random) {
        	// randomly choose numExercises exercises from the hits
        	var numHits = $hits.length;
        	var $hitsOnly = {};
        	for (var k=0; k<numHits; k++) {
        		$hitsOnly[k] = $hits[k];
        	}
            $sampledHitsOnly = wertiview.lib.sampleFromObjectProps($hitsOnly, numExercises);
            var i = 0;
            for (var k in $sampledHitsOnly) {
            	$hits[i] = $sampledHitsOnly[k];
            	i++;
            }
        }
        else if (choiceMode == wertiview.pref_first) {
        	offset = wertiview.getFirstOffset();
        }
        else if (choiceMode == wertiview.pref_intervals){
        	step = wertiview.getIntervalSize();
        }
        else {
        	// we should never get here
        	wertiview.ajaxError();
        }
		
		// FIXME this loop cannot be replaced with one over hitList as in the 
		// other topics because that breaks the line marked with '**' below
        var i = -1;
		$hits.each( function () {
			i++;
			if (numExercises <= 0 || i < offset || (i-offset) % step != 0) {
				return;
			}
			numExercises--;
			
			$(this).data('wertiview-original-text', $(this).html());
			$(this).data('wertiview-target-text', $(this).text());
			
			// if this contains links, skip
			if ($(this).find('a').length > 0) {
				return;
			}
			
			// look at all element and text node children
			$(this).contents().each( function () {
				// if they contain non-whitespace
				if(/[^\t\n\r ]/.test(this.data)) {
					var $node = $(this);
					
					// turn text nodes into spans
					if (this.nodeType == 3) {
						$(this).wrap( function () {
							return '<span class="wertiviewtoken wertiviewtextnode"></span>';
						});
						$node = $(this).parent();
					}
				}
			});
			
			$cloneofq = $(this).clone();
			
			// combine all wertiviewtokens (normally just at the end of question)
			// into one node
			$restofq = $('<span class="wertiviewrestofq">');
			$cloneofq.children().each( function() {
				var isChunk = false;
				for (className in wertiview.whquestions.relevantChunks) {
					if ($(this).hasClass(className)) {
						isChunk = true;
					}
				}
				// if this child is not itself a chunk, doesn't have any parents as chunks, 
				// and doesn't have any children as chunk
				if (!isChunk && $(this).parents(findTargetsString).length == 0 && $(this).find(findTargetsString).length == 0) {
					// figure out whether to add a space, crudely; if
					// - there is a token to the left
					// - this token contains alpha characters
					// - this token doesn't start with '
					if ($restofq.text() != '' && $(this).text().match(/\w/) && $(this).text()[0] != "'") {
							$restofq.append(' ');
					}
					$restofq.append($(this).text());
					$(this).remove();
				}
			});
			$cloneofq.append($restofq);
			
			// create a list with all of the nodes for randomizing
			var childrenList = [];
			$cloneofq.children().each( function() {
				childrenList.push($(this));				
			});
			
			// figure out when it would be best to skip this question, currently:
			// - there are more than 10 tokens
			if (childrenList.length > 10) {
				return;	
			}
			
			// - there is no question mark at the end (suggests sentence segmentation failure)
			if (!$cloneofq.text().match(/\?\s*$/)) {
				return;
			}
			
			// - there is more than one wh-word
			if ($cloneofq.find('.wertiviewWH, .wertiviewWHS').length > 1) {
				return;
			}
			
			// - if intervening text prevent the restofq bit from working properly
			if (wertiview.whquestions.compareFormat($(this).text()) != wertiview.whquestions.compareFormat($cloneofq.text())) {
				return;
			}

			// randomize list
			wertiview.lib.shuffleList(childrenList);
			
			// replace the current tokens with the randomized ones
			$(this).empty();
			
			for(var j = 0; j < childrenList.length; j++) {
				var $node = childrenList[j];
				// ** FIXME (see above)
				$(this).append($node);
				
				$node.addClass('clozeStyleNode');

				$node.data('wertiview-cloze-target', $node.parent().attr('id') + "-input");
			}

			// create input field
			var $input = $('<input>');
			$input.attr('type', 'text');
			$input.attr('id', $(this).attr('id') + '-input');
			$input.addClass('clozeStyleInputAdjust');
			$input.addClass('clozeStyleInputUnknown');
			$input.addClass('wertiviewinput');
			$input.data('wertiviewanswer', $(this).text());
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
		});
		
		$('body').delegate('span.wertiviewQ span.wertiviewchunk', 'click', {context: contextDoc}, wertiview.whquestions.clozeSpanHandler);
		$('body').delegate('span.wertiviewQ span.wertiviewtoken', 'click', {context: contextDoc}, wertiview.whquestions.clozeSpanHandler);
		$('body').delegate('span.wertiviewQ span.wertiviewrestofq', 'click', {context: contextDoc}, wertiview.whquestions.clozeSpanHandler);
		$('body').delegate('span.wertiviewcheck', 'click', {context: contextDoc}, wertiview.whquestions.clozeCheckHandler);
		$('body').delegate('span.wertiviewclear', 'click', {context: contextDoc}, wertiview.whquestions.clozeClearHandler);
		$('body').delegate('span.wertiviewhint', 'click', {context: contextDoc}, wertiview.whquestions.clozeHintHandler);
		$('body').delegate('input.wertiviewinput', 'keyup keydown blur', {context: contextDoc}, wertiview.whquestions.clozeWidthHandler);
	},
	
	clozeSpanHandler: function(event) {
		var contextDoc = event.data.context;
		
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		// not one of the immediate children in the question (pass request on)
		if (!$(this).data('wertiview-cloze-target')) {
			return true;
		}
		
		var $input = $('#' + $(this).data('wertiview-cloze-target'));
		
		var currentText = $input.val();
		var lastChar = currentText.charAt(currentText.length - 1);
		// add a space if the text is not currently empty and we're adding a non-textnode span and the last character isn't 
		// space (since we don't need two) or apostrophe (the only textnode span I can think of where we don't want a trailing
		// space)
		if (currentText != '' && !lastChar.match(/[ ']/)) {
			currentText += ' ';
		}		
		currentText += $(this).text();
		
		$input.val(currentText);
		$input.trigger('keyup');
	
		return false;
	},
	
	clozeCheckHandler: function(event) {
		var contextDoc = event.data.context;
		
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		var $qParent = $(this).parents('.wertiviewQ').eq(0);
		var $input = $qParent.find('.wertiviewinput').eq(0);
	
		var currentText = $input.val();
		var targetText = $qParent.data('wertiview-target-text');

		currentText = wertiview.whquestions.compareFormat(currentText);
		targetText = wertiview.whquestions.compareFormat(targetText);
		
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
		var contextDoc = event.data.context;
		
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		var $qParent = $(this).parents('.wertiviewQ').eq(0);
	
		var currentText = $(this).val();
		var targetText = $qParent.data('wertiview-target-text');
		
		$qParent.empty();
		$qParent.html($qParent.data('wertiview-original-text'));
		$qParent.addClass('clozeStyleProvided');
		
		return false;
	},
	
	clozeClearHandler: function(event) {
		var contextDoc = event.data.context;
		
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		var $qParent = $(this).parents('.wertiviewQ').eq(0);
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
	},

	compareFormat: function(text) {
		return text.toLowerCase().replace(/[^\w]/g, '');
	}
	};
}); // REMOVE-WITH-MAVEN-REPLACER-PLUGIN
