
	wertiview.serestar = {	

	// for documentation of these variables, see pos.js
	MAX_MC: 5,
	
	// map from hit text to distractor
	hit2distractor: {},
	
	remove: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		$('body').undelegate('span.wertiviewtoken', 'click', wertiview.serestar.clickHandler);
		$('body').undelegate('select.wertiviewinput', 'change', wertiview.serestar.clozeInputHandler);
		$('body').undelegate('span.wertiviewhint', 'click', wertiview.serestar.clozeHintHandler);
		$('body').undelegate('input.wertiviewinput', 'change', wertiview.serestar.clozeInputHandler);
		$('body').undelegate('input.wertiviewhint', 'click', wertiview.serestar.clozeHintHandler);

		$('.wertiviewinput').each( function() {
			$(this).replaceWith($(this).data('wertiviewanswer'));
		});
		$('.wertiviewhint').remove();
	},

	colorize: function(contextDoc) {
		var jQuery = wertiview.jQuery;
        var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
        $.fn = $.prototype = jQuery.fn;        
        
		var topic = $('body').data('wertiview-topic');
		
		$('span.wertiviewSer').addClass('colorizeStyleSer');
		$('span.wertiviewEstar').addClass('colorizeStyleEstar');
	},
	
	colorizeSpan: function(span, topic, index) {
		span.find('span.wertiviewSer').addClass('colorizeStyleSer');
		span.find('span.wertiviewEstar').addClass('colorizeStyleEstar');
	},

	click: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
		$.fn = $.prototype = jQuery.fn;
		
		// change all wertiviewtoken spans to mouseover pointer
		$('span.wertiviewtoken').css({'cursor': 'pointer'});
		
		// randomly pick wertiviewSer or wertiviewEstar
		var binaryRand = wertiview.lib.getRandom(1);
		var clickClass = 'wertiviewSer';
		if (binaryRand == 1) {
			clickClass = 'wertiviewEstar';
		}
		$('body').data('wertiviewClickClass', clickClass);

		// add instructions
		var message = 'Please click on all forms of <b>';
		
		if (clickClass == 'wertiviewSer') {
			message += 'ser';
		} else {
			message += 'estar';
		}
		message += '</b>.';
		wertiview.notification.instDialog(message, contextDoc);

		// handle POS clicking
		$('body').delegate('span.wertiviewtoken', 'click', {context: contextDoc}, wertiview.serestar.clickHandler);
	},

	clickHandler: function(event) {
		var jQuery = wertiview.jQuery;
		var contextDoc = event.data.context;
        var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
        $.fn = $.prototype = jQuery.fn;
        
        var clickClass = $('body').data('wertiviewClickClass');
                
		if($(this).hasClass(clickClass)) {
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
		var $hits = $('span.wertiviewSer, span.wertiviewEstar');
		
		// TODO: see if there's a better way to figure out
		// environment-related character encoding problems
		var inExtension = wertiview.lib.inExtension();
		
		var hitList = [];
		wertiview.serestar.hit2distractor = {};
		$hits.each( function() {
			var hittext = $(this).text().toLowerCase();
			var distractor;
			if ($(this).hasClass('wertiviewSer')) {
				distractor = wertiview.serestar.serToEstar[hittext];
				if (distractor == undefined) {
					distractor = wertiview.serestar.serToEstar[wertiview.lib.encodeUTF8(hittext)];
				}
			} else {
				distractor = wertiview.serestar.estarToSer[hittext];
				if (distractor == undefined) {
					distractor = wertiview.serestar.estarToSer[wertiview.lib.encodeUTF8(hittext)];
				}
			}

			if (!inExtension) {
				distractor = wertiview.lib.decodeUTF8(distractor);
			}
			if (distractor == null) {
				return;
			}

			wertiview.serestar.hit2distractor[hittext] = distractor;
			hitList.push($(this));
		});
		
		wertiview.activity.mc(contextDoc, hitList, 
				wertiview.serestar.clozeInputHandler, 
				wertiview.serestar.clozeHintHandler, 
				wertiview.serestar.mcGetOptions, 
				wertiview.serestar.mcGetCorrectAnswer);
	},
	
	mcGetOptions: function($hit, capType){
		var options;
		var hittext = $hit.text().toLowerCase();
		var distractor = wertiview.serestar.hit2distractor[hittext];
		if ($hit.hasClass('wertiviewSer')) {
			options = [hittext, distractor];
		} else {
			options = [distractor, hittext];
		}
		return options;
	},
	
	mcGetCorrectAnswer: function($hit, capType){
		return $hit.text().toLowerCase();		
	},
	
	cloze: function(contextDoc) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,contextDoc||window.content.document); };
        $.fn = $.prototype = jQuery.fn;

		// get potential spans
		var $hits = $('span.wertiviewSer, span.wertiviewEstar');
		
		var hitList = []; 
		$hits.each( function() {
			hitList.push($(this));				
		});

		wertiview.activity.cloze(contextDoc, hitList, 
				wertiview.serestar.clozeInputHandler, 
				wertiview.serestar.clozeHintHandler, 
				wertiview.serestar.mcGetCorrectAnswer);
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
	},
	
	serToEstar: {'ser':	'estar',
		'sido':	'estado',
		'siendo':	'estando',
		'soy':	'estoy',
		'eres':	'estás',
		'es':	'está',
		'somos':	'estamos',
		'sois':	'estáis',
		'son':	'están',
		'fui':	'estuve',
		'fuiste':	'estuviste',
		'fue':	'estuvo',
		'fuimos':	'estuvimos',
		'fuisteis':	'estuvisteis',
		'fueron':	'estuvieron',
		'era':	'estaba',
		'eras':	'estabas',
		'era':	'estaba',
		'éramos':	'estábamos',
		'erais':	'estabais',
		'eran':	'estaban',
		'seré':	'estaré',
		'serás':	'estarás',
		'será':	'estará',
		'seremos':	'estaremos',
		'seréis':	'estaréis',
		'serán':	'estarán',
		'sería':	'estaría',
		'serías':	'estarías',
		'sería':	'estaría',
		'seríamos':	'estaríamos',
		'seríais':	'estaríais',
		'serían':	'estarían',
		'sea':	'esté',
		'seas':	'estés',
		'sea':	'esté',
		'seamos':	'estemos',
		'seáis':	'estéis',
		'sean':	'estén',
		'fuera':	'estuviera',
		'fuese':	'estuviese',
		'fueras':	'estuvieras',
		'fueses':	'estuvieses',
		'fuera':	'estuviera',
		'fuese':	'estuviese',
		'fuéramos':	'estuviéramos',
		'fuésemos':	'estuviésemos',
		'fuerais':	'estuvierais',
		'fueseis':	'estuvieseis',
		'fueran':	'estuvieran',
		'fuesen':	'estuviesen',
		'fuere':	'estuviere',
		'fueres':	'estuvieres',
		'fuere':	'estuviere',
		'fuéremos':	'estuviéremos',
		'fuereis':	'estuviereis',
		'fueren':	'estuvieren'},
		
	estarToSer: {'estar':	'ser',
		'estado':	'sido',
		'estando':	'siendo',
		'estoy':	'soy',
		'estás':	'eres',
		'está':	'es',
		'estamos':	'somos',
		'estáis':	'sois',
		'están':	'son',
		'estuve':	'fui',
		'estuviste':	'fuiste',
		'estuvo':	'fue',
		'estuvimos':	'fuimos',
		'estuvisteis':	'fuisteis',
		'estuvieron':	'fueron',
		'estaba':	'era',
		'estabas':	'eras',
		'estaba':	'era',
		'estábamos':	'éramos',
		'estabais':	'erais',
		'estaban':	'eran',
		'estaré':	'seré',
		'estarás':	'serás',
		'estará':	'será',
		'estaremos':	'seremos',
		'estaréis':	'seréis',
		'estarán':	'serán',
		'estaría':	'sería',
		'estarías':	'serías',
		'estaría':	'sería',
		'estaríamos':	'seríamos',
		'estaríais':	'seríais',
		'estarían':	'serían',
		'esté':	'sea',
		'estés':	'seas',
		'esté':	'sea',
		'estemos':	'seamos',
		'estéis':	'seáis',
		'estén':	'sean',
		'estuviera':	'fuera',
		'estuviese':	'fuese',
		'estuvieras':	'fueras',
		'estuvieses':	'fueses',
		'estuviera':	'fuera',
		'estuviese':	'fuese',
		'estuviéramos':	'fuéramos',
		'estuviésemos':	'fuésemos',
		'estuvierais':	'fuerais',
		'estuvieseis':  'fueseis',
		'estuvieran':   'fueran',
		'estuviesen':   'fuesen',
		'estuviere':	'fuere',
		'estuvieres':	'fueres',
		'estuviere':	'fuere',
		'estuviéremos':	'fuéremos',
		'estuviereis':	'fuereis',
		'estuvieren':	'fueren'}
	};

