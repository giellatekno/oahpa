package werti.util;

import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.uima.jcas.JCas;

import com.google.gson.Gson;

/**
 * JSONEnhancer produces a JSON array containing each enhanced span from a CAS
 * containing a sequence of &lt;e&gt; spans and Enhancements.
 *  
 * @author Adriane Boyd
 *
 */
public class JSONEnhancer {
	private JCas cas;
	private String activity;
	
	/** 
	 * @param cCas CAS with annotations for the topic
	 * @param aActivity Activity name
	 */
	public JSONEnhancer(final JCas cCas, String aActivity) {
		cas = cCas;
		activity = aActivity;
	}
	
	/**
	 * Converts a CAS with Enhancements to an array of enhanced spans 
	 * in JSON format.
	 * 
	 * @return JSON string of CAS including enhancements
	 */
	public String enhance() {
		String enhanced = EnhancerUtils.casToEnhanced(cas, activity);
		enhanced = enhancedToJSON(enhanced);		
		
		return enhanced;
	}
	
	/**
	 * Converts a string containing a sequence of <e></e> enhanced spans into 
	 * a JSON array where each array element is wrapped with a <span> that 
	 * minimizes layout changes.
	 * 
	 * @param enhanced string to enhance
	 * @return JSON string of CAS including enhancements
	 */
	private String enhancedToJSON(String enhanced) {
		// TODO: the regex at least should be moved somewhere where it can be shared between this function
		// and the EnhanceXMLAnnotator (the EnhanceXML UIMA annotations are no longer useful because we've
		// inserted the enhancements)

		// regex to match the <e> enhance spans
		Pattern enhancePatt = Pattern.compile("<e ([^>]*)>(.*?)</e>", Pattern.DOTALL);
		Pattern counterPatt = Pattern.compile("id=\"(\\d+)\"");
		Matcher enhanceMatcher = enhancePatt.matcher(enhanced);

		HashMap<Integer, String> newNodes = new HashMap<Integer, String>();

		while (enhanceMatcher.find()) {
			// find index
			Matcher counterMatcher = counterPatt.matcher(enhanceMatcher.group(1));
			int counter = 0;
			if (counterMatcher.find()) {
				counter = Integer.parseInt(counterMatcher.group(1));
			}
			// wrap outer span around each group
			// TODO: calling addSpanStyle for each group is probably very inefficient, 
			// need to fix preserveWhitespace problem with Jsoup
			//newNodes.put(counter, EnhancerUtils.addSpanStyle("<span class=\"werti\" style=\"" + EnhancerUtils.addedSpanStyle + "\">" + enhanceMatcher.group(2) + "</span>"));
			newNodes.put(counter, "<span class=\"wertiview\" style=\"" + EnhancerUtils.addedSpanStyle + "\">" + enhanceMatcher.group(2) + "</span>");
		}

		// convert the list of new nodes to JSON and return
		Gson gson = new Gson();
		return gson.toJson(newNodes);
	}
}
