package werti.uima.enhancer;

import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

import org.apache.log4j.Logger;

import org.apache.uima.UimaContext;
import org.apache.uima.analysis_component.JCasAnnotator_ImplBase;

import org.apache.uima.analysis_engine.AnalysisEngineProcessException;

import org.apache.uima.cas.FSIndex;

import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceInitializationException;

import werti.uima.types.Enhancement;

import werti.uima.types.annot.Token;
import werti.util.EnhancerUtils;

/**
 * An enhancer that takes an annotated cas and marks puts enhancement annotations
 * in the same cas where Part-of-Speech tags meet the tags it's been given in the
 * paramaters.
 *
 * @author Aleksandar Dimitrov
 * @version 0.1
 */

public class PoSEnhancer extends JCasAnnotator_ImplBase {
	private static final Logger log =
		Logger.getLogger(PoSEnhancer.class);
	
	private List<String> tags;
	
	@Override
	public void initialize(UimaContext context)
			throws ResourceInitializationException {
		super.initialize(context);
		tags = Arrays.asList(((String)context.getConfigParameterValue("tags")).split(","));
	}

	/**
	 * Iterate over all <tt>Token</tt>s in the CAS and match their PoStags.
	 *
	 * If they belong to the target class, then annotate them with enhancement
	 * annotations.
	 *
	 * @param cas The document's CAS.
	 */
	@SuppressWarnings("unchecked")
	public void process(JCas cas) throws AnalysisEngineProcessException {
		int id = 0;
		log.debug("Starting enhancement");
		
		final FSIndex textIndex = cas.getAnnotationIndex(Token.type);
		final Iterator<Token> tit = textIndex.iterator();

		log.debug("Feature Structure index size: " + textIndex.size());

		Token t; // token pointer

		while (tit.hasNext()) {
			t = tit.next();
			if (t.getTag() == null) {
				log.debug("Encountered token with NULL tag");
				continue;
			}
			if (tags.contains(t.getTag())) {
				final Enhancement e = new Enhancement(cas);
				e.setBegin(t.getBegin());
				e.setEnd(t.getEnd());

				id++;
				e.setEnhanceStart("<span id=\"" + EnhancerUtils.get_id("WERTi-span",id) + "\">");
				e.setEnhanceEnd("</span>");

				if (log.isTraceEnabled()) {
					log.trace("Enhanced " + t.getCoveredText()
							+ " with tag "
							+ t.getTag()
							+ " with id "
							+ id);
				}
				e.addToIndexes();
			}
		}
		log.debug("Finished enhancement");
	}
}
