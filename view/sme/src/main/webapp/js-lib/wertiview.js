var wertiview = {
		jQuery: window.jQuery.noConflict(true),
		serverURL: 'http://sifnos.sfs.uni-tuebingen.de/WERTi',
		
		// PREFERENCES (for compatibility with add-on)
		// In the webapp, the preferences all have constant default values.
		// TODO provide interface to change the preferences in the webapp
		
		// preferences
		pref_fixedNumber: 0,
		pref_percentage: 1,
		pref_random: 0,
		pref_first: 1,
		pref_intervals: 2,
		
		
		// return the preference 'fixed number or percentage' as an integer
		getFixedOrPercentage: function(){
			return wertiview.pref_fixedNumber;
		},
		
		// return the preference 'fixedNumberOfExercises'
		getFixedNumberOfExercises: function() {
			return 20;
		},
		
		// return the preference 'proportionOfExercises' as a decimal (0-1)
		getProportionOfExercisesDec: function() {
			return 1.0;
		},
		
		
		// return the choice mode as an integer
		getChoiceMode: function() {
			return wertiview.pref_random;
		},
		
		// return the preference 'firstOffset'
		getFirstOffset: function() {
			return 0;
		},
		
		// return the preference 'intervalSize'
		getIntervalSize: function() {
			return 1;
		},
		
		// return the preference 'noncountRatio' as a decimal between 0 and 1
		getNoncountRatioDec: function() {
			return 0.2;
		},

		
		// illegal value for a preference (e.g., user edited about:config)
		prefError: function(message) {       
			//wertiview.toolbar.enableRunButton();
			//wertiview.blur.remove();

			if (!message) {
				message = "The preferences have illegal values. This should never happen in the web interface of VIEW.";
			}
			
			var error = {};
			error.message = message;
			error.getMessage = function() { return this.message; };
			
			throw error;
		}
};
