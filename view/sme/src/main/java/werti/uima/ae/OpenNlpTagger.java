package werti.uima.ae;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import opennlp.tools.postag.POSTaggerME;

import org.apache.log4j.Logger;
import org.apache.uima.UimaContext;
import org.apache.uima.analysis_component.JCasAnnotator_ImplBase;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.cas.text.AnnotationIndex;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceInitializationException;

import werti.WERTiContext;
import werti.WERTiContext.WERTiContextException;
import werti.uima.types.annot.SentenceAnnotation;
import werti.uima.types.annot.Token;

/**
 * Annotator wrapper for OpenNLP tagger.
 * 
 * Depends on {@link Token} and {@link SentenceAnnotation} annotation from 
 * {@link OpenNlpTokenizer} and {@link OpenNlpSentenceDetector}.
 * 
 * @author Adriane Boyd
 */
public class OpenNlpTagger extends JCasAnnotator_ImplBase {
	private static Map<String, POSTaggerME> taggers;	
	private static final Logger log = Logger.getLogger(OpenNlpTagger.class);
	
	@Override
	public void initialize(UimaContext aContext)
			throws ResourceInitializationException {
		super.initialize(aContext);
		
		try {
			taggers = new HashMap<String, POSTaggerME>();
			taggers.put("en", WERTiContext.request(POSTaggerME.class, "en"));
		} catch (WERTiContextException wce) {
			throw new ResourceInitializationException(wce);
		}
	}
	
	@SuppressWarnings("unchecked")
	@Override
	public void process(JCas jcas) throws AnalysisEngineProcessException {
		log.debug("Starting tag annotation");
		
		final AnnotationIndex sentIndex = jcas.getAnnotationIndex(SentenceAnnotation.type);
		final AnnotationIndex tokenIndex = jcas.getAnnotationIndex(Token.type);
				
		final Iterator<SentenceAnnotation> sit = sentIndex.iterator();
		
		final String lang = jcas.getDocumentLanguage();
		
		POSTaggerME tagger;
		
		if (taggers.containsKey(lang)) {
			tagger = taggers.get(lang);
		} else {
			log.error("No tagger for language: " + lang);
			throw new AnalysisEngineProcessException();
		}
		
		while (sit.hasNext()) {
			List<Token> tokenlist = new ArrayList<Token>();
			List<String> tokens = new ArrayList<String>();
			
			final Iterator<Token> tit = tokenIndex.subiterator(sit.next());
			
			while (tit.hasNext()) {
				final Token t = tit.next();
				tokenlist.add(t);
				tokens.add(t.getCoveredText());
			}
		
			List<String> tags = tagger.tag(tokens);
			
			for (int i = 0; i < tags.size(); i++) {
				tokenlist.get(i).setTag(tags.get(i));
			}
		}
		
		log.debug("Finished tag annotation");
	}
}
