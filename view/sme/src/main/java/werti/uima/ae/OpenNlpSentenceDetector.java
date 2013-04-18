package werti.uima.ae;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import opennlp.tools.sentdetect.SentenceDetectorME;

import org.apache.log4j.Logger;
import org.apache.uima.UimaContext;
import org.apache.uima.analysis_component.JCasAnnotator_ImplBase;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.cas.FSIndex;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceInitializationException;

import werti.WERTiContext;
import werti.WERTiContext.WERTiContextException;
import werti.uima.types.annot.SentenceAnnotation;
import werti.uima.types.annot.Token;

/**
 * Wrapper for OpenNLP sentence detector.
 * 
 * Depends on {@link Token} Token annotation from {@link OpenNlpTokenizer}.
 * 
 * @author Adriane Boyd
 */
public class OpenNlpSentenceDetector extends JCasAnnotator_ImplBase {

	private static Map<String, SentenceDetectorME> detectors;
	private static final Logger log =
		Logger.getLogger(OpenNlpTokenizer.class);
	
	private static final Pattern trailingSpacePattern = Pattern.compile("\\s+$");
	private static final Pattern sentenceBeginPattern = Pattern.compile("[\\p{L}\\p{N}\\p{P}]");
	
	@Override
	public void initialize(UimaContext aContext)
			throws ResourceInitializationException {
		super.initialize(aContext);
		
		try {
			detectors = new HashMap<String, SentenceDetectorME>();
			detectors.put("en", WERTiContext.request(SentenceDetectorME.class, "en"));
		} catch (WERTiContextException wce) {
			throw new ResourceInitializationException(wce);
		}
	}
	
	@SuppressWarnings("unchecked")
	@Override
	public void process(JCas jcas) throws AnalysisEngineProcessException {
		log.debug("Starting sentence detection");
		
		String text = jcas.getDocumentText();
		StringBuilder rtext = new StringBuilder();
		rtext.setLength(text.length());
		
		// create an empty document
		for (int i = 0; i < text.length(); i++) {
			rtext.setCharAt(i, ' ');
		}
		
		// put tokens in their proper positions in this empty document
		final FSIndex tagIndex = jcas.getAnnotationIndex(Token.type);
		final Iterator<Token> tit = tagIndex.iterator();
		
		while (tit.hasNext()) {
			Token t = tit.next();
			rtext.replace(t.getBegin(), t.getEnd(), t.getCoveredText());
		}
		
		final String lang = jcas.getDocumentLanguage();
		SentenceDetectorME detector;
		
		if (detectors.containsKey(lang)) {
			detector = detectors.get(lang);
		} else {
			log.error("No tagger for language: " + lang);
			throw new AnalysisEngineProcessException();
		}

		int[] offsets = detector.sentPosDetect(rtext.toString());
		
		// iterate one past the end of offsets.length and use the end of 
		// rtext instead of offsets[i] in the last iteration
		for (int i = 0; i <= offsets.length; i++) {
			int currentOffset = i == offsets.length ? rtext.length() : offsets[i]; 
			int previousOffset = i > 0 ? offsets[i - 1] : 0;
			
			String sentenceStr = rtext.substring(previousOffset, currentOffset);
			Matcher beginMatcher = sentenceBeginPattern.matcher(sentenceStr);
			Matcher endMatcher = trailingSpacePattern.matcher(sentenceStr);
			int sentenceBegin = beginMatcher.find() ? beginMatcher.start() : 0;
			int sentenceEnd = endMatcher.find() ? endMatcher.start() : sentenceStr.length();
			int start = previousOffset + sentenceBegin;
			int end = previousOffset + sentenceEnd;
			SentenceAnnotation sentence = new SentenceAnnotation(jcas, start, end);
			sentence.addToIndexes();
		} 
		
		log.debug("Finished sentence detection");
	}	
}
