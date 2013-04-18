package werti.uima.ae;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import opennlp.tools.tokenize.TokenizerME;

import org.apache.log4j.Logger;
import org.apache.uima.UimaContext;
import org.apache.uima.analysis_component.JCasAnnotator_ImplBase;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.cas.FSIndex;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceInitializationException;

import werti.WERTiContext;
import werti.WERTiContext.WERTiContextException;
import werti.uima.types.annot.RelevantText;
import werti.uima.types.annot.Token;

/**
 * Wrapper for OpenNLP tokenizer.
 * 
 * @author Adriane Boyd
 */
public class OpenNlpTokenizer extends JCasAnnotator_ImplBase {

	private static Map<String, TokenizerME> tokenizers;
	private static final Logger log =
		Logger.getLogger(OpenNlpTokenizer.class);

	@Override
	public void initialize(UimaContext aContext)
			throws ResourceInitializationException {
		super.initialize(aContext);
		
		try {
			tokenizers = new HashMap<String, TokenizerME>();
			tokenizers.put("en", WERTiContext.request(TokenizerME.class, "en"));
		} catch (WERTiContextException wce) {
			throw new ResourceInitializationException(wce);
		}
	}

	
	@SuppressWarnings("unchecked")
	@Override
	public void process(JCas jcas) throws AnalysisEngineProcessException {
		log.debug("Starting token annotation");
		
		String text = jcas.getDocumentText();
		StringBuilder rtext = new StringBuilder();
		rtext.setLength(text.length());
		
		// create an empty document
		for (int i = 0; i < text.length(); i++) {
			rtext.setCharAt(i, ' ');
		}
		
		// put relevant text spans in their proper positions in this empty document
		final FSIndex tagIndex = jcas.getAnnotationIndex(RelevantText.type);
		final Iterator<RelevantText> tit = tagIndex.iterator();
		
		while (tit.hasNext()) {
			RelevantText t = tit.next();
			rtext.replace(t.getBegin(), t.getEnd(), t.getCoveredText());
		}
		
		final String textString = rtext.toString();
		final String lang = jcas.getDocumentLanguage();
		
		String[] tokens = null;
		
		if (tokenizers.containsKey(lang)) {
			tokens = tokenizers.get(lang).tokenize(textString);
		} else {
			log.error("No tokenizer for language: " + lang);
			throw new AnalysisEngineProcessException();
		}
		
		int skew = 0;
		
		for (String token : tokens) {
			// include all tokens that don't consist of whitespace, i.e., prevent
			// unicode non-breaking space from becoming a token
			if (token.matches("[^\\p{Z}]+")) {
				final Token t = new Token(jcas);
				skew = textString.indexOf(token, skew);
				final int start = skew;
				skew += token.length();
				t.setBegin(start);
				t.setEnd(start + token.length());
				
				int tlen = t.getCoveredText().length();

				// check for leading or trailing unicode quotes or possessives
				// that the OpenNlp model doesn't separate from the adjacent words
				if (tlen > 1 && t.getCoveredText().substring(0, 1).matches("‘|“")) {
					t.setBegin(start + 1);
					
					final Token t2 = new Token(jcas);
					t2.setBegin(start);
					t2.setEnd(start + 1);
					t2.addToIndexes();
				} else if (tlen > 1 && t.getCoveredText().substring(tlen - 1, tlen).matches("’|”")) {					
					t.setEnd(start + token.length() - 1);	
					
					final Token t2 = new Token(jcas);
					t2.setBegin(start + token.length() - 1);
					t2.setEnd(start + token.length());
					t2.addToIndexes();
				} else if (tlen > 2 && t.getCoveredText().substring(tlen - 2, tlen).matches("’s")) {
					t.setEnd(start + token.length() - 2);
					
					final Token t2 = new Token(jcas);
					t2.setBegin(start + token.length() - 2);
					t2.setEnd(start + token.length() - 1);
					t2.addToIndexes();
					
					final Token t3 = new Token(jcas);
					t3.setBegin(start + token.length() - 1);
					t3.setEnd(start + token.length());
					t3.addToIndexes();
				}
				
				t.addToIndexes();
				if (log.isTraceEnabled()) {
					log.trace("Token: " + t.getBegin() + " " + t.getCoveredText() + " " + t.getEnd());
				}
			}
		}
		
		log.debug("Finished token annotation");
	}
}
