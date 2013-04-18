package werti.uima.enhancer;

import java.util.Iterator;

import org.apache.log4j.Logger;
import org.apache.uima.analysis_component.JCasAnnotator_ImplBase;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.cas.FSIndex;
import org.apache.uima.jcas.JCas;

import werti.uima.types.Enhancement;
import werti.uima.types.annot.RelevantText;
import werti.util.EnhancerUtils;

/**
 * An enhancer that adds classes for HTML content types.
 * Only for development purposes.
 *
 * @author Adriane Boyd
 * @version 0.1
 */

public class HTMLContentTypeEnhancer extends JCasAnnotator_ImplBase {
	private static final Logger log =
		Logger.getLogger(HTMLContentTypeEnhancer.class);

	/**
	 * Iterate over all <tt>RelevantText</tt>s in the CAS and examine their 
	 * htmlContentTypes.
	 *
	 * @param cas The document's CAS.
	 */
	@SuppressWarnings("unchecked")
	public void process(JCas cas) throws AnalysisEngineProcessException {
		int id = 0;
		log.debug("Starting HTML content type enhancement");
		
		final FSIndex textIndex = cas.getAnnotationIndex(RelevantText.type);
		final Iterator<RelevantText> tit = textIndex.iterator();

		log.debug("Feature Structure index size: " + textIndex.size());

		RelevantText t;
		
		while (tit.hasNext()) {
			t = tit.next();
			if (t.getHtmlContentType() == null) {
				log.debug("Encountered token with NULL tag");
				continue;
			}

			final Enhancement e = new Enhancement(cas);
			e.setBegin(t.getBegin());
			e.setEnd(t.getEnd());
			e.setRelevant(true);

			id++;
			e.setEnhanceStart("<span id=\"" + EnhancerUtils.get_id("WERTi-span", id) + 
					"\" class=\"wertiview" + t.getHtmlContentType() + "\">");
			e.setEnhanceEnd("</span>");

			if (log.isTraceEnabled()) {
				log.trace("Enhanced " + t.getCoveredText()
						+ " with tag "
						+ t.getHtmlContentType()
						+ " with id "
						+ id);
			}
			e.addToIndexes();
		}
		log.debug("Finished HTML content type enhancement");
	}
}
