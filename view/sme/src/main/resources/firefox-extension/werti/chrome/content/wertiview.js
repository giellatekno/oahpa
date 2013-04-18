// Credits:
//
// The namespace setup is from:
// http://www.softwareishard.com/blog/planet-mozilla/firefox-extensions-global-namespace-pollution/
// 
// The jQuery setup is from:
// http://forums.mozillazine.org/viewtopic.php?f=19&t=1460255

// The only global object for this extension.
var wertiview = {};

(function() {
	// Registration
	var namespaces = [];
	this.ns = function(fn) {
		var ns = {};
		namespaces.push(fn, ns);
		return ns;
	};
	// Initialization
	this.initialize = function() {
		for (var i=0; i<namespaces.length; i+=2) {
			var fn = namespaces[i];
			var ns = namespaces[i+1];
			fn.apply(ns);
		}
	};
	// Clean up
	this.shutdown = function() {
		window.removeEventListener("load", wertiview.initialize, false);
		window.removeEventListener("unload", wertiview.shutdown, false);
	};
	// Register handlers to maintain extension life cycle.
	window.addEventListener("load", wertiview.initialize, false);
	window.addEventListener("unload", wertiview.shutdown, false);
}).apply(wertiview);

wertiview.ns(function() {
	wertiview = {

	// TODO switch back to sifnos before reintegrating this branch
	serverURL: 'http://localhost:8080/VIEW',
	servletURL: '',

	VERSION: '',
	versionChecked: false,
	nativeJSON: null,
	
	// preferences
	pref_fixedNumber: 0,
	pref_percentage: 1,
	pref_random: 0,
	pref_first: 1,
	pref_intervals: 2,

	// load libraries and add listeners
	load: function(context){
		// generate servlet URL
		wertiview.servletURL = wertiview.serverURL + '/VIEW';
		
		// load jQuery and extensions
		var loader = Components.classes["@mozilla.org/moz/jssubscript-loader;1"].getService(Components.interfaces.mozIJSSubScriptLoader);
		loader.loadSubScript("chrome://view/content/jquery-1.4.2.min.js", context);
		
		var sss = Components.classes["@mozilla.org/content/style-sheet-service;1"]
									 .getService(Components.interfaces.nsIStyleSheetService);
		var ios = Components.classes["@mozilla.org/network/io-service;1"]
									 .getService(Components.interfaces.nsIIOService);
		
		var uri = ios.newURI("chrome://view/content/view.css", null, null);
		if(!sss.sheetRegistered(uri, sss.USER_SHEET)) {
			sss.loadAndRegisterSheet(uri, sss.USER_SHEET);
		}
		
		// load JSON (built-in JSON available only for FF 3.5+,
		// nsIJSON is available for FF 3.0+)
		wertiview.nativeJSON = Components.classes["@mozilla.org/dom/json;1"].createInstance(Components.interfaces.nsIJSON);
		
		// get current version number
		// (from https://developer.mozilla.org/en/Code_snippets/Miscellaneous)
		try {
			// Firefox 4 and later; Mozilla 2 and later
			Components.utils.import("resource://gre/modules/AddonManager.jsm");
			AddonManager.getAddonByID("view@sfs.uni-tuebingen.de", function(addon) {
				wertiview.VERSION = addon.version;
				wertiview.checkVersion();
			});
		} catch (ex) {
			// Firefox 3.6 and before; Mozilla 1.9.2 and before
			var em = Components.classes["@mozilla.org/extensions/manager;1"]
			.getService(Components.interfaces.nsIExtensionManager);
			wertiview.VERSION = em.getItemForID("view@sfs.uni-tuebingen.de").version;
			wertiview.checkVersion();
		}

		// load jQuery
		var jQuery = window.jQuery.noConflict(true);
		wertiview.jQuery = jQuery;

		// add listeners
		wertiview.addListeners();
	},
	
	

	// return the preferences as a map with keys 'language', 'topic', 
	// 'activity', and 'version'
	getOptions: function() {
		var prefservice = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
		var prefs = prefservice.getBranch("extensions.wertiview.");
		var options = {};
		options['language'] = prefs.getCharPref("language");
		options['topic'] = prefs.getCharPref("topic");
		options['activity'] = prefs.getCharPref("activity");
		options['version'] = prefs.getCharPref("version");
		return options;
	},
	
	
	// return the preference 'fixed number or percentage' as an integer
	getFixedOrPercentage: function(){
		var prefservice = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
		var prefs = prefservice.getBranch("extensions.wertiview.");
		
		var fixedOrPercentage = prefs.getIntPref("fixedOrPercentage");
		return fixedOrPercentage;
	},
	
	// return the preference 'fixedNumberOfExercises'
	getFixedNumberOfExercises: function() {
		var prefservice = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
		var prefs = prefservice.getBranch("extensions.wertiview.");
		
		var fixedNumberOfExercises = prefs.getIntPref("fixedNumberOfExercises");
		return fixedNumberOfExercises;
	},
	
	// return the preference 'proportionOfExercises' as a decimal (0-1)
	getProportionOfExercisesDec: function() {
		var prefservice = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
		var prefs = prefservice.getBranch("extensions.wertiview.");
		
		var percentage = prefs.getIntPref("proportionOfExercises");
		return percentage / 100.0;
	},
	
	
	// return the choice mode as an integer
	getChoiceMode: function() {
		var prefservice = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
		var prefs = prefservice.getBranch("extensions.wertiview.");
		
		var choiceMode = prefs.getIntPref("choiceMode");
		return choiceMode;
	},
	
	// return the preference 'firstOffset'
	getFirstOffset: function() {
		var prefservice = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
		var prefs = prefservice.getBranch("extensions.wertiview.");
		
		var firstOffset = prefs.getIntPref("firstOffset");
		return firstOffset;
	},
	
	// return the preference 'intervalSize'
	getIntervalSize: function() {
		var prefservice = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
		var prefs = prefservice.getBranch("extensions.wertiview.");
		
		var intervalSize = prefs.getIntPref("intervalSize");
		return intervalSize;
	},
	
	// return the preference 'noncountRatio' as a decimal between 0 and 1
	getNoncountRatioDec: function() {
		var prefservice = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
		var prefs = prefservice.getBranch("extensions.wertiview.");
		
		var noncountRatio = prefs.getIntPref("noncountRatio");
		return noncountRatio / 100.0;
	},

	
	// illegal value for a preference (e.g., user edited about:config)
	prefError: function(message) {       
		wertiview.toolbar.enableRunButton();
		wertiview.blur.remove();

		if (message) {
			alert(message);
		}
		else {
			alert("The preferences have illegal values. Please go to 'Options > Addons' and change the VIEW preferences.");
		}
	},
	
	
	setOptions: function(language, topic, activity) {
		var prefservice = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
		var prefs = prefservice.getBranch("extensions.wertiview.");
		
		prefs.setCharPref("language", language);
		prefs.setCharPref("topic", topic);
		prefs.setCharPref("activity", activity);
	},

	setVersion: function(version) {
		var prefservice = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
		var prefs = prefservice.getBranch("extensions.wertiview.");

		prefs.setCharPref("version", version);
	},
	
	

	addListeners: function() {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,context||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		var appcontent = document.getElementById("appcontent");
		if(appcontent) {
			appcontent.addEventListener("DOMContentLoaded", wertiview.runIfEnabled, true);
		}

		var container = gBrowser.tabContainer;
		container.addEventListener("TabSelect", wertiview.tabSwitch, false);
	},

	runIfEnabled: function(aEvent) {
		var prefservice = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
		var prefs = prefservice.getBranch("extensions.wertiview.");

		if(wertiview.isTopLevelDocument(aEvent.originalTarget)) {
			if (prefs.getBoolPref("enabled")) {
				wertiview.activity.add(aEvent.originalTarget);
			}
		}
	},

	isTopLevelDocument: function(doc) {
		var browsers = gBrowser.browsers;
		for (var i = 0; i < browsers.length; i++) {
			if (doc == browsers[i].contentDocument) {
				return true;
			}
		}
		return false;
	},

	// update toolbar when the user switches tabs
	tabSwitch: function() {
		var browser = gBrowser.selectedBrowser;

		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,context||window.content.document); };
		$.fn = $.prototype = jQuery.fn;

		// if wertiview was run on this page
		var savedOptions = {};
		savedOptions['language'] = $('body').data('wertiview-language');
		savedOptions['topic'] = $('body').data('wertiview-topic');
		savedOptions['activity'] = $('body').data('wertiview-activity');
		
		// change the toolbar menus to the previously run topic/activity
		if (savedOptions['language'] && savedOptions['topic'] && savedOptions['activity']) {
			wertiview.setOptions(savedOptions['language'], savedOptions['topic'], savedOptions['activity']);
			wertiview.toolbar.initialize();
			wertiview.toolbar.enableRestoreButton();
		} else {
			wertiview.toolbar.disableRestoreButton();
		}
	},

	// open URLs when certain topics are selected in menus
	goToPage: function(event, page) {
		var url = '';
		switch(page) {
			case 'help':
				url = wertiview.serverURL + '/index.jsp?content=activities';
				break;
			default:
				url = wertiview.serverURL;
		}

		window._content.document.location = url;
		window.content.focus();
	},

	// return the URL of the document for logging purposes
	getURL: function(contextDoc) {
		// figure out which document we're working with
		var doc = contextDoc;
		if (!contextDoc) {
			doc = window.content.document;
		}

		//return doc.location.href;
		return doc.baseURI;
	},
	
	// display an about page based on information from install.rdf
	openAbout: function() {
        try {
        	Components.utils.import("resource://gre/modules/AddonManager.jsm");
            AddonManager.getAddonByID("view@sfs.uni-tuebingen.de", function(addon) {
                openDialog("chrome://mozapps/content/extensions/about.xul", "",
                		"chrome,centerscreen,modal", addon);
            });
        } catch(ex) {
        	var gExtensionManager = Components.classes["@mozilla.org/extensions/manager;1"]
        	.getService(Components.interfaces.nsIExtensionManager);
        	openDialog("chrome://mozapps/content/extensions/about.xul", "",
        			"chrome,centerscreen,modal", "urn:mozilla:item:view@sfs.uni-tuebingen.de", gExtensionManager.datasource);
        }		
	},
	
	// display changelog on upgrade (adapted from the NoScript extension)
	checkVersion: function() {
		options = wertiview.getOptions();
		if (!wertiview.versionChecked && wertiview.VERSION != options['version']) {
			wertiview.setVersion(wertiview.VERSION);
			var windowMediator = Components.classes["@mozilla.org/appshell/window-mediator;1"]
			.getService(Components.interfaces.nsIWindowMediator);
			var browser = windowMediator.getMostRecentWindow(null).getBrowser();

			if (typeof(browser.addTab) != "function") {
				return;
			}

			var b = (browser.selectedTab = browser.addTab()).linkedBrowser;
			b.stop();
			b.webNavigation.loadURI(wertiview.serverURL + '/index.jsp?content=changelog&version=' + wertiview.VERSION, Components.interfaces.nsIWebNavigation.LOAD_FLAGS_NONE, null, null, null);
		}
		wertiview.versionChecked = true;
	}
	};
	
	// delay library loading to improve firefox startup time
	var timer = Components.classes["@mozilla.org/timer;1"]
		.createInstance(Components.interfaces.nsITimer);

	timer.initWithCallback(wertiview.load, 200, Components.interfaces.nsITimer.TYPE_ONE_SHOT);
});
