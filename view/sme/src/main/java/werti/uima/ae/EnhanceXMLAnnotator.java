package werti.uima.ae;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.log4j.Logger;
import org.apache.uima.analysis_component.JCasAnnotator_ImplBase;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.jcas.JCas;
import werti.uima.types.annot.EnhanceXML;

/**
 * Annotate all &lt;e&gt; tags.
 *
 * @author Adriane Boyd
 */

public class EnhanceXMLAnnotator extends JCasAnnotator_ImplBase {
	private static final Logger log =
		Logger.getLogger(EnhanceXMLAnnotator.class);

	/**
	 * Mark up all werti spans.
	 */
	public void process(JCas cas) throws AnalysisEngineProcessException {
		
		log.debug("Starting markup recognition");
		
		final String s = cas.getDocumentText().toLowerCase();

		// regex to match the <e> enhance spans
		Pattern enhancePatt = Pattern.compile("<e( [^>]*)?>(.*?)</e>", Pattern.DOTALL);
		Matcher enhanceMatcher = enhancePatt.matcher(s);
		
		while (enhanceMatcher.find()) {
			// create tag for enhance start tag
			final EnhanceXML starttag = new EnhanceXML(cas);
			starttag.setBegin(enhanceMatcher.start());
			starttag.setEnd(enhanceMatcher.start(2));
			starttag.setTag_name("spanwertiview");
			starttag.addToIndexes();
			
			// create tag for enhance end tag
			final EnhanceXML endtag = new EnhanceXML(cas);
			endtag.setBegin(enhanceMatcher.end(2));
			endtag.setEnd(enhanceMatcher.end());
			endtag.setTag_name("spanwertiview");
			endtag.setClosing(true);
			endtag.addToIndexes();
		}
		
		log.debug("Finished markup recognition");
	}
}
