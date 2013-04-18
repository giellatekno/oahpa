package werti.uima.enhancer;

import java.util.Iterator;

import org.apache.uima.UimaContext;
import org.apache.uima.analysis_component.JCasAnnotator_ImplBase;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.cas.FSIterator;
import org.apache.uima.cas.text.AnnotationIndex;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceInitializationException;
import werti.uima.types.Enhancement;
import werti.uima.types.annot.Token;

/**
 * Hijacks the title attribute to store the base form, infinitive form, and 
 * gerund form for the gerunds topic in order to able to generate the 
 * multiple choice activity (infinitive and gerund displayed in drop-down list) 
 * and the cloze activity (verb provided as base form).
 * 
 * @author Adriane Boyd
 *
 */
public class BaseformPostEnhancer extends JCasAnnotator_ImplBase {
	
	/* (non-Javadoc)
	 * @see org.apache.uima.analysis_component.AnalysisComponent_ImplBase#initialize(org.apache.uima.UimaContext)
	 */
	@Override
	public void initialize(UimaContext context)
			throws ResourceInitializationException {
		super.initialize(context);
	}

	@SuppressWarnings("unchecked")
	@Override
	public void process(JCas cas) throws AnalysisEngineProcessException {
		FSIterator enhanceIter = cas.getAnnotationIndex(Enhancement.type).iterator();
		AnnotationIndex tindex = cas.getAnnotationIndex(Token.type);

		while (enhanceIter.hasNext()) {
			Enhancement e = (Enhancement) enhanceIter.next();
			String baseForm = null;
			String infForm = null;
			String gerForm = null;
			String startTag = e.getEnhanceStart();
			
			// iterate to last token in e
			final Iterator<Token> tit = tindex.subiterator(e);
			Token t = null;
			while (tit.hasNext()) {
				t = tit.next();
			}
			
			// if a final token is found, add base forms, 
			// else remove enhancement (this shouldn't happen!)
			if (t != null) {
				// to-infinitive
				if (startTag.contains("INF")) {
					baseForm = t.getLemma();
					infForm = e.getCoveredText();				
					gerForm = t.getGerund();
					// gerund
				} else if (startTag.contains("GER")) {
					baseForm = t.getLemma();
					infForm = "to " + t.getLemma();
					gerForm = e.getCoveredText();
					// anything else? not interested
				} else {
					continue;
				}
				startTag = startTag.replace(">", " title=\"" + baseForm + ";" + infForm + ";" + gerForm + "\">");
				e.setEnhanceStart(startTag);
			} else {
				e.removeFromIndexes();
			}
		}
	}
}
