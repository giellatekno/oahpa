wertiview.ns(function() {
	wertiview.openid = {
	
	// FOR DOCUMENTATION SEE ALSO: http://openid.net/
	
	getCookie: function(doc, c_name) {
		// we see only the name-value pairs without expiry dates or paths 
		var cookies = doc.cookie.split(";");
		for (var i = 0; i < cookies.length; i++) {
			var equIndex = cookies[i].indexOf("=");
			var name = cookies[i].substr(0, equIndex);
			var value = cookies[i].substr(equIndex + 1);
			name = name.replace(/^\s+|\s+$/g, "");
			if (name == c_name) {
				return unescape(value);
			}
		}
		return null;
	},

	// send the user-supplied identifier to the server
	signIn: function(xulDoc, userSuppliedIdentifier) {
		if (userSuppliedIdentifier === undefined || userSuppliedIdentifier.length == 0) {
			alert("Please enter your OpenID in the text box on the VIEW toolbar.");
			return;
		}
		else {
			//wertiview.toolbar.disableSignInButton();
			wertiview.openid.sendAjaxRequest(userSuppliedIdentifier);
		}
	},
	
	// communicate with the server to perform the OpenID authentication
	sendAjaxRequest: function(userSuppliedIdentifier) {
		var jQuery = wertiview.jQuery;

		/* The reason why this document is JSP and not HTML is simply so it 
		 * sets the JSESSIONID cookie in the browser, which is necessary to be 
		 * able to track the VIEW users. */
		// TODO don't hardcode URL
		var newWindow = window.open("http://localhost:8080/VIEW/openid/pleasewait.jsp");
		var jsessionid = null;
		var done = false;
		setInterval(function() {
			if (!done) {
				jsessionid = wertiview.openid.getCookie(newWindow.content.document, "JSESSIONID");
				if (jsessionid != null) {
					done = true;

					var requestInfo = {};
					requestInfo['type'] = "openid-authentication";
					requestInfo['url'] = userSuppliedIdentifier;
					requestInfo['document'] = jsessionid;
					requestInfo['version'] = wertiview.VERSION;

					var request = {
						type: "POST",
						url: wertiview.servletURL,
						data: wertiview.nativeJSON.encode(requestInfo),
						processData: false,
						timeout: 60000,
						success: function(response, textStatus, xhr) { 
							if (response) {
								wertiview.openid.showPasswordPrompt(userSuppliedIdentifier, response, newWindow);
							} else {
								wertiview.openid.ajaxError(xhr, "nodata");
							}
						},
						error: wertiview.openid.ajaxError
					};
					jQuery.ajax(request);

				}
			}
		}, 500);
	},

	ajaxError: function(xhr, textStatus, errorThrown) {
		wertiview.toolbar.enableSignInButton();
		
		// TODO write error messages that are transparent for the user
		if (!xhr || !textStatus) {
			alert("OpenID: The VIEW server encountered an error."
				+ "\nxhr: " + wertiview.lib.obj2str(xhr)
				+ "\ntextStatus: " + textStatus
				+ "\nerrorThrown: " + errorThrown);
			return;
		}

		switch(textStatus) {
			case "nodata":
				alert("OpenID: The VIEW server is currently unavailable.");
				break;
			case "timeout":
				alert("OpenID: The VIEW server is taking too long to respond.");
				break;
			case "error":
				switch (xhr.status) {
					case 490:
						alert("OpenID: The VIEW server no longer supports this version of the VIEW extension.\nPlease check for a new version of the add-on in the Tools->Add-ons menu!");
						break;
					case 491:
						alert("OpenID: The topic selected isn't available.\nPlease select a different topic from the toolbar menu.");
						break;
					case 492:
						alert("OpenID: The topic selected isn't available for the language selected.\nPlease select a different language or topic from the toolbar menu.");
						break;
					default:
						alert("OpenID: The VIEW server encountered an error."
								+ "\nxhr: " + wertiview.lib.obj2str(xhr)
								+ "\ntextStatus: " + textStatus
								+ "\nerrorThrown: " + errorThrown);
						break;
				}
				break;
			default:
				alert("OpenID: The VIEW server encountered an error."
						+ "\nxhr: " + wertiview.lib.obj2str(xhr)
						+ "\ntextStatus: " + textStatus
						+ "\nerrorThrown: " + errorThrown);
				break;
		};
	},
	
	// show the user the password prompt from their OpenID Provider
	showPasswordPrompt: function(userSuppliedIdentifier, response, newWindow) {
		var jQuery = wertiview.jQuery;
		var $ = function(selector,context){ return new jQuery.fn.init(selector,context||newWindow.content.document); };
		$.fn = $.prototype = jQuery.fn;

		var parser = new DOMParser();
		var newDom = parser.parseFromString(response, "text/html");
		
		// fiddle the response's <head> and <body> into the current page
		$('head', newDom).each(function() {
			$('head').append(this);
		});
		$('body').replaceWith($('body', newDom));
		// redirect automatically
		newWindow.content.document.forms['openid-form-redirection'].submit();

		wertiview.toolbar.enableSignInButton();
	},
	
	signOut: function(xulDoc) {
		window.open(wertiview.serverURL + "/openid/logout.jsp");
	}
	
	};
}); // REMOVE-WITH-MAVEN-REPLACER-PLUGIN
