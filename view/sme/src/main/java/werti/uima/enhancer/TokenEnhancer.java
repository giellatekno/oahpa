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
 * An enhancement class that puts WERTi-<tt>&lt;span&gt;</tt>s around <em>all</em>
 * tokens and optionally gives them the attribute 'wertiviewhit' when they belong to a given
 * POS.
 *
 * @author Aleksandar Dimitrov
 * @author Adriane Boyd
 * @version 0.1
 */

public class TokenEnhancer extends JCasAnnotator_ImplBase {
	private static final Logger log =
		Logger.getLogger(TokenEnhancer.class);
	
	private List<String> tags;
	private boolean useLemmaFilter;
	
	@Override
	public void initialize(UimaContext context)
			throws ResourceInitializationException {
		super.initialize(context);
		tags = Arrays.asList(((String)context.getConfigParameterValue("Tags")).split(","));
		useLemmaFilter = (Boolean) context.getConfigParameterValue("UseLemmaFilter");
	}

	/**
	 * Iterate over all tokens and put a span around them. If a token matches one of the given
	 * POS tags, then mark it up as a hit.
	 *
	 */
	@SuppressWarnings("unchecked")
	public void process(JCas cas) throws AnalysisEngineProcessException {
		int id = 0;
		log.debug("Starting enhancement");

		final FSIndex textIndex = cas.getAnnotationIndex(Token.type);
		final Iterator<Token> tit = textIndex.iterator();

		Token t;

		while (tit.hasNext()) {
			t = tit.next();
			// enhance all non-punctuation tokens
			if (t.getCoveredText().matches(".*[^\\p{P}].*")) {
				final Enhancement e = new Enhancement(cas);
				e.setBegin(t.getBegin());
				e.setEnd(t.getEnd());

				id++;
				final int hit;

				if (t.getTag() == null) {
					log.debug("Encountered token with NULL tag");
					hit = 0;
				} else if (tags.contains(t.getTag())) {
					if (useLemmaFilter) {
						if (t.getLemma() == null || t.getLemma().equals("")) {
							hit = 0;
						} else {
							hit = 1;
						}
					} else {
						hit = 1;
					}
				} else {
					hit = 0;
				}

				String hitclass = "";
				if (hit == 1) {
					hitclass = "wertiviewhit";
					e.setRelevant(true);
				} else {
					e.setRelevant(false);
				}
				e.setEnhanceStart("<span id=\"" + EnhancerUtils.get_id("WERTi-span", id) 
						+ "\" class=\"wertiviewtoken " + hitclass + "\">");
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
