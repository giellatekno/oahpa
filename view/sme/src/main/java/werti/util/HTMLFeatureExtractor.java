package werti.util;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.Iterator;
import java.util.regex.Pattern;

import org.apache.commons.lang.StringEscapeUtils;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.nodes.Node;
import org.jsoup.nodes.TextNode;
import org.jsoup.parser.Tag;
import org.jsoup.select.Elements;

/**
 * Feature extractor for HTML structure detection.
 * 
 * @author Adriane Boyd
 * 
 */
public class HTMLFeatureExtractor {
	public static String className = "werti";

	// from boilerpipe, for tokenizer
	private static final Pattern PAT_WORD_BOUNDARY = Pattern.compile("\\b");
	private static final Pattern PAT_NOT_WORD_BOUNDARY = Pattern
			.compile("[\u2063]*([\\\"'\\.,\\!\\@\\-\\:\\;\\$\\?\\(\\)/])[\u2063]*");

	public static void main(String args[]) throws IOException {
		URL url = null;
		File file = null;

		boolean useUrl = false;

		if (args.length > 0) {
			if (useUrl) {
				url = new URL(args[0]);
			} else {
				file = new File(args[0]);
			}
		}

		if (url == null && file == null) {
			System.err.println("Please provide a URL or file!");
			return;
		}

		Document htmlDoc;
		if (useUrl) {
			htmlDoc = Jsoup.parse(url, 10000);
		} else {
			htmlDoc = Jsoup.parse(file, null);
		}

		// add <span class="werti"></span> tags around any plain text
		// segments in the document
		markTextNodes(htmlDoc, htmlDoc.body());

		// for each of these spans, extract features:

		// find all spans just added around text
		Elements wertiTextSpans = htmlDoc.getElementsByClass(className);

		// TODO: calculate the relevant token, density, etc. counts once
		// for each span and cache them here rather than doing the same
		// work repeatedly in extractFeatures() below

		// create an empty span to use as padding for the beginning/end
		// surrounding context
		Element emptyElement = new Element(Tag.valueOf("span"),
				htmlDoc.baseUri());

		// iterate over the spans with one span before/after as context
		Iterator<Element> it = wertiTextSpans.listIterator();

		Element prevElement = emptyElement;
		Element currentElement = it.next();
		Element nextElement = it.hasNext() ? it.next() : emptyElement;

		extractFeatures(prevElement, currentElement, nextElement);

		if (nextElement != emptyElement) {
			while (it.hasNext()) {
				prevElement = currentElement;
				currentElement = nextElement;
				nextElement = it.next();
				extractFeatures(prevElement, currentElement, nextElement);
			}
			prevElement = currentElement;
			currentElement = nextElement;
			nextElement = emptyElement;
			extractFeatures(prevElement, currentElement, nextElement);
		}
	}

	private static void extractFeatures(Element prev, Element e, Element next) {
		final Elements parents = e.parents();

		// for debugging:
		System.out.println(e.html());

		System.out.print(isInP(parents) + ",");
		System.out.print(isImmediateParentP(e) + ",");
		System.out.print(getNumWords(prev) + ",");
		System.out.print(getNumWords(e) + ",");
		System.out.print(getNumWords(next) + ",");
		System.out.println(getAnnotation(parents));
	}

	/**
	 * Find the closest parent that contains an L3S-GN1 annotation in the form
	 * for x-nc-sel[0-5], return x-nc-sel0 if none found.
	 *
	 * For reference:
	 * 
	 * x-nc-sel0       Not content
	 * x-nc-sel1       Headline
	 * x-nc-sel2       Full text
	 * x-nc-sel3       Supplemental
	 * x-nc-sel4       Related content
	 * x-nc-sel5       Comments
	 * 
	 * We probably want to collapse some of these and translate them into
	 * more meaningful class names like: HEADER, TEXT, SUPP, RELATED, 
	 * OTHER, etc.
	 * 
	 * @param parents
	 * @return
	 */
	private static String getAnnotation(Elements parents) {
		String ann = "x-nc-sel0";

		for (Element p : parents) {
			if (p.attr("class") != null
					&& p.attr("class").matches("x-nc-sel[0-5]")) {
				return p.attr("class");
			}
		}

		return ann;
	}

	private static boolean isInP(Elements parents) {
		for (Element p : parents) {
			if (p.tagName().toLowerCase().equals("p")) {
				return true;
			}
		}

		return false;
	}

	private static boolean isImmediateParentP(Element e) {
		if (e.parent().tagName().toLowerCase().equals("p")) {
			return true;
		}

		return false;
	}

	private static int getNumWords(Element e) {
		return tokenize(e.text()).length;
	}

	/**
	 * Traverses the HTML document tree adding <span class="className"> spans
	 * around all text nodes and converting HTML entities to unicode characters.
	 * 
	 * @param doc
	 *            the Jsoup document
	 * @param node
	 *            the node to traverse
	 */
	private static void markTextNodes(Document doc, Node node) {
		// if this is a non-empty text node, add an <span class="className">
		// tag around it
		if (node instanceof TextNode) {
			if (!((TextNode) node).isBlank()) {
				Element eElem = doc.createElement("span");
				eElem.addClass(className);
				eElem.text(StringEscapeUtils.unescapeHtml(((TextNode) node)
						.text()));
				node.replaceWith(eElem);
			}
		} else { // look at almost all the child nodes
			for (Node child : node.childNodes()) {
				if (!child.nodeName().matches("script")
						&& !child.nodeName().matches("noscript")
						&& !child.nodeName().matches("form")
						&& !child.nodeName().matches("object")
						&& !child.nodeName().matches("embed")
						&& !child.nodeName().matches("head")) {
					markTextNodes(doc, child);
				}
			}
		}
	}

	/**
	 * Simple tokenizer copied from boilerpipe:
	 * 
	 * Tokenizes the text and returns an array of tokens.
	 * 
	 * @param text
	 *            The text
	 * @return The tokens
	 */
	private static String[] tokenize(final String text) {
		return PAT_NOT_WORD_BOUNDARY
				.matcher(PAT_WORD_BOUNDARY.matcher(text).replaceAll("\u2063"))
				.replaceAll("$1").replaceAll("[ \u2063]+", " ").trim()
				.split("[ ]+");
	}
}
