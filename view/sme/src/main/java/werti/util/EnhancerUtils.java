package werti.util;

import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;

import org.apache.commons.lang.StringEscapeUtils;
import org.apache.uima.cas.FSIndex;
import org.apache.uima.jcas.JCas;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

import werti.uima.types.Enhancement;
import werti.uima.types.annot.RelevantText;

/**
 * Methods for converting a CAS with annotation to a document
 * with HTML enhancements.  These methods are used by both the
 * {@link JSONEnhancer} and the {@link HTMLEnhancer}.
 * 
 * @author Adriane Boyd
 */
public class EnhancerUtils {
	public static final String addedSpanStyle = "display: inline; background-image: none; padding: 0px; margin: 0px; color: inherit; font: inherit; font-size: 100%; position: relative; top: 0px; left: 0px;";
	
	// need those two to supply JS-annotations with IDs.
	public static String get_id(String spanClass, int id) {
		return spanClass + "-" + id;
	}

    /**
     * Adds a layout-preserving style attribute to all spans in the HTML fragment.
     * 
     * @param html an HTML fragment
     * @return the HTML fragment with added style attributes
     */
	public static String addSpanStyle(String html) {
		// add layout-preserving style to all spans from cas
		Document doc = Jsoup.parse("<html><head></head><body>" + html + "</body></html>");
		doc.select("span").attr("style", EnhancerUtils.addedSpanStyle);
		
		html = doc.body().html();
		return html;
	}

	/**
	 * Inserts HTML enhancements into the text of the CAS, returning the 
	 * entire document as a string.
	 * 
	 * @param cas 
	 * @param activity
	 * @return Document with enhancements
	 */
	public static String casToEnhanced(JCas cas, String activity) {
		final String docText = cas.getDocumentText();
		final StringBuilder rtext = new StringBuilder(docText);
		
		HashMap<Integer, String> insertedTags = EnhancerUtils.getInsertedTags(cas, activity);
		HashSet<Integer> relevantTextPositions = EnhancerUtils.getRelevantTextPositions(cas);

		// obtain sorted key set
		LinkedList<Integer> positions = new LinkedList<Integer>(insertedTags.keySet());
		Collections.sort(positions);

		// loop over position hash and insert enhancement tags into document text using skew
		// while also converting any non-EnhanceXML characters to entities
		int skew = 0;
		int prevpos = 0;
		String escapedTextSubstring;

		for ( Integer pos : positions ) {
			String textSubstring = rtext.substring(prevpos + skew, pos + skew);
			escapedTextSubstring = EnhancerUtils.escapeSubstring(rtext, relevantTextPositions, prevpos, pos, skew);

			rtext.replace(prevpos + skew, pos + skew, escapedTextSubstring);
			skew += escapedTextSubstring.length() - textSubstring.length();

			String insert = insertedTags.get(pos);
			rtext.insert(pos + skew, insert);
			skew += insert.length();

			prevpos = pos;
		}

		escapedTextSubstring = EnhancerUtils.escapeSubstring(rtext, relevantTextPositions, prevpos, rtext.length() - skew, skew);
		rtext.replace(prevpos + skew, rtext.length(), escapedTextSubstring);

		return rtext.toString();
	}
	
	@SuppressWarnings("unchecked")
	public static HashMap<Integer, String> getInsertedTags(JCas cas, String activity) {
    	final FSIndex tagIndex = cas.getAnnotationIndex(Enhancement.type);
    	final Iterator<Enhancement> eit = tagIndex.iterator();

    	HashMap<Integer, String> insertedTags = new HashMap<Integer, String>();

    	// TODO: make sure this maintains the correct order of closing tags

    	// collect all enhancements on positions
    	while (eit.hasNext()) {
    		Enhancement e = eit.next();
    		
    		if (e.getRelevant() || activity.matches("click")) {
    			// add beginning of enhancement to the position hash
    			int begin = e.getBegin();
    			if ( ! insertedTags.containsKey(begin)) {
    				insertedTags.put(begin, e.getEnhanceStart());
    			} else {
    				insertedTags.put(begin, insertedTags.get(begin) + e.getEnhanceStart());
    			}

    			// add end of enhancement to the position hash
    			int end = e.getEnd();
    			if ( ! insertedTags.containsKey(end)) {
    				insertedTags.put(end, e.getEnhanceEnd());
    			} else {
    				insertedTags.put(end, e.getEnhanceEnd() + insertedTags.get(end));
    			}
    		}
    	}

    	return insertedTags;
	}
	
	/**
	 * Returns the set of positions in the document that contain relevant text
	 * (i.e. not HTML or other markup).
	 * 
	 * @param cas document
	 * @return set of relevant positions
	 */
	@SuppressWarnings("unchecked")
	public static HashSet<Integer> getRelevantTextPositions(JCas cas) {		
		final FSIndex textIndex = cas.getAnnotationIndex(RelevantText.type);
		final Iterator<RelevantText> tit = textIndex.iterator();
		HashSet<Integer> positions = new HashSet<Integer>();
		
		while (tit.hasNext()) {
			final RelevantText t = tit.next();
			for (int i = t.getBegin(); i < t.getEnd(); i++) {
				positions.add(i);
			}
		}
		
		return positions;
	}
	
	/**
	 * Converts the unicode relevant text characters in rtext to their
	 * escaped HTML counterparts.  Non-relevant text is left unchanged.
	 * 
	 * @param rtext the document
	 * @param RelevantTextPositions positions containing text that should be escaped
	 * @param start start position in original document
	 * @param end end position in original document
	 * @param skew skew from previously inserted elements
	 * @return the text with non-markup non-ASCII characters escaped to HTML
	 */
	public static String escapeSubstring(StringBuilder rtext, HashSet<Integer> RelevantTextPositions, int start, int end, int skew) {
		String textSubstring = rtext.substring(start + skew, end + skew);
		String escapedTextSubstring = "";
		
		for (int i = 0; i < textSubstring.length(); i++) {
			String singleChar = rtext.substring(start + skew + i, start + skew + i + 1);
			if (RelevantTextPositions.contains(start + i)) {
				singleChar = StringEscapeUtils.escapeHtml(singleChar);
			}
			escapedTextSubstring = escapedTextSubstring.concat(singleChar);
		}
		
		return escapedTextSubstring;
	}
}
