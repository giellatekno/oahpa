package werti.uima.ae;

import java.util.Iterator;

import org.apache.log4j.Logger;
import org.apache.uima.analysis_component.JCasAnnotator_ImplBase;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.cas.FSIndex;
import org.apache.uima.jcas.JCas;
import werti.uima.types.annot.EnhanceXML;
import werti.uima.types.annot.RelevantText;

/**
 * Generic relevance annotator.
 *
 * Marks all parts of the document that aren't between EnhanceXML (&lt;e&gt;) tags as irrelevant.
 * 
 * @author Adriane Boyd
 */
public class GenericRelevanceAnnotator extends JCasAnnotator_ImplBase {
	private static final Logger log =
		Logger.getLogger(GenericRelevanceAnnotator.class);

	/**
	 * Marks all parts of the document annotated as inside EnhanceXML tags by EnhanceXMLAnnotator as relevant.
	 * 
	 * @param cas The document's cas.
	 */
	@SuppressWarnings("unchecked")
	public void process(JCas cas) throws AnalysisEngineProcessException {
		log.debug("Starting relevance annotation");
		final FSIndex tagIndex = cas.getAnnotationIndex(EnhanceXML.type);
		final Iterator<EnhanceXML> tit = tagIndex.iterator();
		
		if (!tit.hasNext()) {
			return;
		}
		
		EnhanceXML tag = tit.next();
		if (tag == null) {
			throw new AnalysisEngineProcessException(
					new NullPointerException("No EnhanceXML tags were found!"));
		}
		
		while (tit.hasNext()) {
			final RelevantText rt = new RelevantText(cas);
			
			// get type/end info from the current tag
			rt.setBegin(tag.getEnd());

			// move to the next tag
			tag = tit.next();
			
			// get begin info from the next tag
			rt.setEnd(tag.getBegin());
			
			if (tag.getClosing()) {
			
				rt.addToIndexes();
			}	
		}
		
		log.debug("Finished relevance annotation");
	}
}
