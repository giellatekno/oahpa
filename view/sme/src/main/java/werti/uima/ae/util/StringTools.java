package werti.uima.ae.util;

import org.apache.log4j.Logger;

/**
 * String normalization tools.  Currently only used in passive
 * sentence conversions.
 * 
 * @author Adriane Boyd
 *
 */
public class StringTools {
	private static final Logger log = Logger.getLogger(StringTools.class);
	
	public static String capitalizeFirstLetter(String s) {
		for (int i = 0; i < s.length(); i++) {
			String l = s.substring(i, i + 1);
			if (l.matches("[^\\p{Z}]")) {
				s = s.substring(0, i) + l.toUpperCase() + s.substring(i + 1);
				break;
			}
		}
		
		return s;		
	}
	
	public static String uncapitalizeFirstLetter(String s) {
		for (int i = 0; i < s.length(); i++) {
			String l = s.substring(i, i + 1);
			if (l.matches("[^\\p{Z}]")) {
				s = s.substring(0, i) + l.toLowerCase() + s.substring(i + 1);
				break;
			}
		}
		
		return s;		
	}
	
	public static String fixPunctuationWhitespace(String s) {
		// replace space before periods
		s = s.replaceAll(" \\.", ".");
		
		// replace space before commas
		s = s.replaceAll(" ,", ",");
		
		// replace space before question marks
		s = s.replaceAll(" \\?", "?");
		
		// replace space before exclamation points
		s = s.replaceAll(" !", "!");
		
		// TODO: do something about bracketing punctuation?
		return s;
	}
}