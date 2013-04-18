package werti.uima.ae;

import java.io.StringReader;
import java.util.Iterator;

import org.apache.log4j.Logger;
import org.apache.uima.UimaContext;
import org.apache.uima.analysis_component.JCasAnnotator_ImplBase;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.cas.text.AnnotationIndex;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceInitializationException;

import werti.uima.ae.util.Morpha;
import werti.uima.types.annot.Token;

/**
 * Wrapper for jflex Morpha implementation from Stanford CoreNLP.
 * 
 * @author Adriane Boyd
 *
 */
public class MorphaLemmatizer extends JCasAnnotator_ImplBase {
	
	private static final Logger log = Logger.getLogger(MorphaLemmatizer.class);
	
	private Morpha lexer;
	
	/* (non-Javadoc)
	 * @see org.apache.uima.analysis_component.AnalysisComponent_ImplBase#initialize(org.apache.uima.UimaContext)
	 */
	@Override
	public void initialize(UimaContext context)
			throws ResourceInitializationException {
		super.initialize(context);
		
		lexer = new Morpha(System.in);
	}
	
	@SuppressWarnings("unchecked")
	@Override
	public void process(JCas jcas) throws AnalysisEngineProcessException{
		log.debug("Starting lemma annotation");
		
		final AnnotationIndex tokenIndex = jcas.getAnnotationIndex(Token.type);
				
		Iterator<Token> tit = tokenIndex.iterator();

		while (tit.hasNext()) {
			Token t = tit.next();
			String tag = t.getTag();
			
			// hack to get morpha to work with the non-standard
			// lingpipe tags
			if (tag != null && tag.matches("v[bdh]g")) {
				tag = "vvg";
			}
			
			String lemma = stem(t.getCoveredText(), tag);
			t.setLemma(lemma);
		}
		
		log.debug("Finished lemma annotation");
	}
	
	/** Lemmatize the word, being sensitive to the tag, using the
	 *  passed in lexer.
	 *  
	 *  This code is adapted from Stanford CoreNLP (GPL).
	 */
	private String stem(String word, String tag) {
		boolean wordHasForbiddenChar = word.indexOf('_') >= 0 ||
		word.indexOf(' ') >= 0;
		String quotedWord = word;
		if (wordHasForbiddenChar) {
			try {
				// choose something unlikely. Devangari!
				quotedWord = quotedWord.replaceAll("_", "\u0960");
				quotedWord = quotedWord.replaceAll(" ", "\u0961");
			} catch (Exception e) {
				System.err.println("stem: Didn't work");
			}
		}
		String wordtag = quotedWord + "_" + tag;
		try {
			lexer.setOption(1, true);  // always lowercase?
			lexer.yyreset(new StringReader(wordtag));
			lexer.yybegin(Morpha.scan);
			String wordRes = lexer.next();
			lexer.next(); // go past tag
			if (wordHasForbiddenChar) {
				try {
					System.err.println("Restoring forbidden chars");
					wordRes = wordRes.replaceAll("\u0960", "_");
					wordRes = wordRes.replaceAll("\u0961", " ");
				} catch (Exception e) {
					System.err.println("stem: Didn't work");
				}
			}
			return wordRes;
		} catch (Throwable e) {
			System.err.println("Morphology.stem() had error on word " + word + "/" +
					tag);
			e.printStackTrace();
			return word;
		}
	}

}
