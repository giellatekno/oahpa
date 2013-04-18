package werti.uima.ae.util;

import werti.uima.types.annot.Token;

/**
 * Convert pronouns between subject and object forms.  (For use in
 * passive sentence conversions.)
 * 
 * @author Adriane Boyd
 *
 */
public class PronounConverter {

	public PronounConverter() {
	}

	public String subjToObj(Token t) {
		if (t.getCoveredText().matches("(?i)I")) {
			return "me";
		} else if (t.getCoveredText().matches("(?i)he")) {
			return "him";
		} else if (t.getCoveredText().matches("(?i)she")) {
			return "her";
		} else if (t.getCoveredText().matches("(?i)we")) {
			return "us";
		} else if (t.getCoveredText().matches("(?i)they")) {
			return "them";
		} else if (t.getCoveredText().matches("(?i)who")) {
			return "who";
		}
		
		return t.getCoveredText();
	}
	
	public String objToSubj(Token t) {
		if (t.getCoveredText().matches("(?i)me")) {
			return "I";
		} else if (t.getCoveredText().matches("(?i)him")) {
			return "he";
		} else if (t.getCoveredText().matches("(?i)her")) {
			return "she";
		} else if (t.getCoveredText().matches("(?i)us")) {
			return "we";
		} else if (t.getCoveredText().matches("(?i)them")) {
			return "they";
		} else if (t.getCoveredText().matches("(?i)whom")) {
			return "who";
		}
		
		return t.getCoveredText();
	}
}