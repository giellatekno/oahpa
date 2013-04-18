package werti.util;

import org.apache.commons.lang.StringEscapeUtils;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.nodes.Node;
import org.jsoup.nodes.TextNode;

/**
 * Methods needed for processing HTML input.
 * 
 * @author Adriane Boyd
 *
 */
public class HTMLUtils {
	// random temporary class name used to avoid Jsoup whitespace preservation
	// problem with non-HTML <e> tag
	public static String className = "PCZRlWLK";
	
    /**
     * Traverses the HTML document tree adding <e> spans around all text nodes
     * and converting HTML entities to unicode characters.
     * 
     * @param doc the Jsoup document
     * @param node the node to traverse
     */	
    public static void markTextNodes(Document doc, Node node) {	
    	// if this is a non-empty text node, add an <e> tag
    	if (node instanceof TextNode) {
    		if (!((TextNode) node).isBlank()) {
    			Element eElem = doc.createElement("span");
    			eElem.addClass(className);
    			eElem.text(StringEscapeUtils.unescapeHtml(((TextNode) node).text()));
    			node.replaceWith(eElem);
    		}
    	} else { // look at almost all the child nodes
    		for (Node child : node.childNodes()) {
    			if(!child.nodeName().matches("script") && !child.nodeName().matches("noscript") && 
    					!child.nodeName().matches("form") && !child.nodeName().matches("object") &&
    					!child.nodeName().matches("embed") && !child.nodeName().matches("head")) {
    				markTextNodes(doc, child);
    			}
    		}
    	}
    }
}
