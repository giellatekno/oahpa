package werti.uima.ae;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import opennlp.tools.chunker.ChunkerME;

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
 * Wrapper for OpenNlp chunker.
 * 
 * Depends on annotation from {@link OpenNlpTokenizer} and {@link OpenNlpTagger}.
 * 
 * @author Adriane Boyd
 *
 */
public class OpenNlpChunker extends JCasAnnotator_ImplBase {

	private Map<String, ChunkerME> chunkers;
	private static final Logger log =
		Logger.getLogger(OpenNlpChunker.class);
	
	/* (non-Javadoc)
	 * @see org.apache.uima.analysis_component.AnalysisComponent_ImplBase#initialize(org.apache.uima.UimaContext)
	 */
	@Override
	public void initialize(UimaContext aContext)
			throws ResourceInitializationException {
		super.initialize(aContext);
		
		try {
			chunkers = new HashMap<String, ChunkerME>();
			chunkers.put("en", WERTiContext.request(ChunkerME.class, "en"));
			chunkers.put("es", WERTiContext.request(ChunkerME.class, "es"));
		} catch (WERTiContextException wce) {
			throw new ResourceInitializationException(wce);
		}
	}

	
	@SuppressWarnings("unchecked")
	@Override
	public void process(JCas jcas) throws AnalysisEngineProcessException {
		log.debug("Starting chunk annotation");
		
		final AnnotationIndex sentIndex = jcas.getAnnotationIndex(SentenceAnnotation.type);
		final AnnotationIndex tokenIndex = jcas.getAnnotationIndex(Token.type);

		final Iterator<SentenceAnnotation> sit = sentIndex.iterator();
		
		final String lang = jcas.getDocumentLanguage();
		ChunkerME chunker;
		
		if (chunkers.containsKey(lang)) {
			chunker = chunkers.get(lang);
		} else {
			log.error("No tagger for language: " + lang);
			throw new AnalysisEngineProcessException();
		}

		while (sit.hasNext()) {
			List<Token> tokenlist = new ArrayList<Token>();
			List<String> tokens = new ArrayList<String>();
			List<String> tags = new ArrayList<String>();
			List<String> chunks;

			final Iterator<Token> tit = tokenIndex.subiterator(sit.next());

			while (tit.hasNext()) {
				Token t = tit.next();
				tokenlist.add(t);
				tokens.add(t.getCoveredText());
				tags.add(t.getTag());
			}

			chunks = (ArrayList<String>) chunker.chunk(tokens, tags);

			for (int i = 0; i < chunks.size(); i++) {
				tokenlist.get(i).setChunk(chunks.get(i));
			}
		}
		
		log.debug("Finished chunk annotation");
	}
}
