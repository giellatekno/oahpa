wertiview.ns(function() {
	wertiview.toolbar = {
	initialize: function() {
		var prefservice = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
		var prefs = prefservice.getBranch("extensions.wertiview.");

		// restore enabled button
		var wertiviewToolbarButton = document.getElementById("wertiview-toolbar-enabled");

		if (prefs.getBoolPref("enabled") == true) {
			//enabledCheckbox.setAttribute("checked", true);
			wertiviewToolbarButton.setAttribute("wertiview-state", "enabled");
		} else {
			//enabledCheckbox.setAttribute("checked", false);
			wertiviewToolbarButton.setAttribute("wertiview-state", "disabled");
		}
		
		// restore language menu
		var lang = prefs.getCharPref("language");
		var languageToolbarMenu = document.getElementById("wertiview-toolbar-language-menu");
		var selectedLanguageElement = document.getElementById("wertiview-toolbar-language-" + lang);
		languageToolbarMenu.selectedItem = selectedLanguageElement;

		// restore topic menu
		var topicToolbarMenu = document.getElementById("wertiview-toolbar-topic-menu");
		var selectedTopicElement = document.getElementById("wertiview-toolbar-topic-" + prefs.getCharPref("topic"));
		topicToolbarMenu.selectedItem = selectedTopicElement;

		// restore activity menu
		var activityToolbarMenu = document.getElementById("wertiview-toolbar-activity-menu");
		var selectedActivityElement = document.getElementById("wertiview-toolbar-activity-" + prefs.getCharPref("activity"));
		activityToolbarMenu.selectedItem = selectedActivityElement;
		
		// disable restore button by default
		wertiview.toolbar.disableRestoreButton();
		
		// update topics for language selection
		wertiview.toolbar.updateTopics(lang);
	},

	toggleEnabled: function() {
		var prefservice = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
		var prefs = prefservice.getBranch("extensions.wertiview.");

		var wertiviewToolbarButton = document.getElementById("wertiview-toolbar-enabled");

		if (prefs.getBoolPref("enabled")) {
			prefs.setBoolPref("enabled", false);
			wertiviewToolbarButton.setAttribute("wertiview-state", "disabled");
		} else {
			prefs.setBoolPref("enabled", true);
			wertiviewToolbarButton.setAttribute("wertiview-state", "enabled");
		}
	},

	setSelection: function(pref, event) {
		var prefservice = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
		var prefs = prefservice.getBranch("extensions.wertiview.");

		prefs.setCharPref(pref, event.target.value);
	},
	
	updateTopics: function(lang) {		
		// TODO: get this info from the server dynamically
		// also include activities?
		if (lang == "en") {
			wertiview.toolbar.enableMenuItem("wertiview-toolbar-topic-Arts");
			wertiview.toolbar.enableMenuItem("wertiview-toolbar-topic-Dets");
			wertiview.toolbar.enableMenuItem("wertiview-toolbar-topic-Gerunds");
			wertiview.toolbar.enableMenuItem("wertiview-toolbar-topic-NounCountability");
			wertiview.toolbar.enableMenuItem("wertiview-toolbar-topic-Passives");
			wertiview.toolbar.enableMenuItem("wertiview-toolbar-topic-PhrasalVerbs");
			wertiview.toolbar.enableMenuItem("wertiview-toolbar-topic-Preps");
			wertiview.toolbar.enableMenuItem("wertiview-toolbar-topic-WhQuestions");
			
			wertiview.toolbar.disableMenuItem("wertiview-toolbar-topic-Konjunktiv");
			wertiview.toolbar.disableMenuItem("wertiview-toolbar-topic-SerEstar");
		} else if (lang == "es") {
			wertiview.toolbar.enableMenuItem("wertiview-toolbar-topic-Dets");
			wertiview.toolbar.enableMenuItem("wertiview-toolbar-topic-Preps");
			wertiview.toolbar.enableMenuItem("wertiview-toolbar-topic-SerEstar");
			
			wertiview.toolbar.disableMenuItem("wertiview-toolbar-topic-Arts");
			wertiview.toolbar.disableMenuItem("wertiview-toolbar-topic-Gerunds");
			wertiview.toolbar.disableMenuItem("wertiview-toolbar-topic-Konjunktiv");
			wertiview.toolbar.disableMenuItem("wertiview-toolbar-topic-NounCountability");
			wertiview.toolbar.disableMenuItem("wertiview-toolbar-topic-Passives");
			wertiview.toolbar.disableMenuItem("wertiview-toolbar-topic-PhrasalVerbs");
			wertiview.toolbar.disableMenuItem("wertiview-toolbar-topic-WhQuestions");
		} else if (lang == "de") {
			wertiview.toolbar.enableMenuItem("wertiview-toolbar-topic-Dets");
			wertiview.toolbar.enableMenuItem("wertiview-toolbar-topic-Konjunktiv");
			wertiview.toolbar.enableMenuItem("wertiview-toolbar-topic-Preps");
			
			wertiview.toolbar.disableMenuItem("wertiview-toolbar-topic-Arts");
			wertiview.toolbar.disableMenuItem("wertiview-toolbar-topic-Gerunds");
			wertiview.toolbar.disableMenuItem("wertiview-toolbar-topic-NounCountability");
			wertiview.toolbar.disableMenuItem("wertiview-toolbar-topic-Passives");
			wertiview.toolbar.disableMenuItem("wertiview-toolbar-topic-PhrasalVerbs");
			wertiview.toolbar.disableMenuItem("wertiview-toolbar-topic-SerEstar");
			wertiview.toolbar.disableMenuItem("wertiview-toolbar-topic-WhQuestions");
		}
		
		// switch to "Pick a Topic" if the selected topic isn't available for
		// the currently selected language
		options = wertiview.getOptions();
		if (document.getElementById('wertiview-toolbar-topic-' + options['topic']).disabled == true) {
			var menu = document.getElementById("wertiview-toolbar-topic-menu");
			var item = document.getElementById("wertiview-toolbar-topic-unselected");
			menu.selectedItem = item;
		}
	},
	
	enableMenuItem: function(id) {
		var item = document.getElementById(id);
		item.disabled = false;
	},
	
	disableMenuItem: function(id) {
		var item = document.getElementById(id);
		item.disabled = true;
	},

	enableRunButton: function() {
		var button = document.getElementById("wertiview-toolbar-single-button");
		button.disabled = false;
	},

	disableRunButton: function(id) {
		var button = document.getElementById("wertiview-toolbar-single-button");
		button.disabled = true;
	},

	enableRestoreButton: function() {
		var button = document.getElementById("wertiview-toolbar-remove-button");
		button.disabled = false;
	},

	disableRestoreButton: function(id) {
		var button = document.getElementById("wertiview-toolbar-remove-button");
		button.disabled = true;
	},
	
	enableSignInButton: function() {
		var button = document.getElementById("wertiview-toolbar-openid-signin");
		button.disabled = false;
	},
	
	disableSignInButton: function() {
		var button = document.getElementById("wertiview-toolbar-openid-signin");
		button.disabled = true;
	},
	
	enableSignOutButton: function() {
		var button = document.getElementById("wertiview-toolbar-openid-signout");
		button.disabled = false;
	},
	
	disableSignOutButton: function() {
		var button = document.getElementById("wertiview-toolbar-openid-signout");
		button.disabled = true;
	}
	};

	// set the appropriate toolbar menu selections
	wertiview.toolbar.initialize();
});
