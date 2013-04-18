package werti.uima.ae;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.annolab.tt4j.DefaultExecutableResolver;
import org.annolab.tt4j.TokenHandler;
import org.annolab.tt4j.TreeTaggerWrapper;
import org.apache.log4j.Logger;
import org.apache.uima.analysis_component.JCasAnnotator_ImplBase;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.cas.text.AnnotationIndex;
import org.apache.uima.jcas.JCas;

import werti.WERTiContext;
import werti.uima.types.annot.SentenceAnnotation;
import werti.uima.types.annot.Token;

/**
 * A TreeTagger wrapper.
 * 
 * Retrieves the Token and Sentence annotations from the cas and sets the lemmas
 * and pos-tags for every token using the TreeTagger for Java (TT4J).
 * 
 * @author Iliana Simova
 * @version 0.1
 */
public class TreeTaggerAnnotator extends JCasAnnotator_ImplBase {

	private static final Logger log =
		Logger.getLogger(TreeTaggerAnnotator.class);

	@SuppressWarnings("unchecked")
	@Override
	public void process(JCas cas) throws AnalysisEngineProcessException {
		AnnotationIndex sent = cas.getAnnotationIndex(SentenceAnnotation.type);
		AnnotationIndex tok = cas.getAnnotationIndex(Token.type);
		Iterator<SentenceAnnotation> sentit = sent.iterator();

		final String lang = cas.getDocumentLanguage();
		
		// TODO: figure out why TreeTaggerWrapper crashes after a while when
		// the model has been loaded in WERTiContext so that the model
		// loading can be moved back to an initialization step
		
		final String modelPath = WERTiContext.context.getRealPath("/") + WERTiContext.p.getProperty("models.base") + WERTiContext.p.getProperty("treetagger-model." + lang);
		final String modelEncoding = WERTiContext.p.getProperty("treetagger-encoding." + lang);
		final String ttPath = WERTiContext.p.getProperty("treetagger-path");
		TreeTaggerWrapper<String> tt = new TreeTaggerWrapper<String>();

		// set the TreeTagger model and encoding
		try {
			tt.setModel(modelPath + ":" + modelEncoding);
		} catch (IOException e) {
			e.printStackTrace();
		}

		// set the TreeTagger path
		DefaultExecutableResolver res = new DefaultExecutableResolver();
		ArrayList<String> paths = new ArrayList<String>();
		paths.add(ttPath);
		res.setAdditionalPaths(paths);
		tt.setExecutableProvider(res);
		log.info("Loaded TreeTagger model for: " + lang);
		
		try {
			List<Token> tokens = new ArrayList<Token>();
			List<String> words = new ArrayList<String>();
			final ArrayList<String> tags = new ArrayList<String>();
			final ArrayList<String> lemmas = new ArrayList<String>();

			tt.setHandler(new TokenHandler<String>() {
				public void token(String token, String pos, String lemma) {
					tags.add(pos);
					lemmas.add(lemma);

				}
			});

			// for every sentence
			while (sentit.hasNext()) {
				Iterator<Token> tokit = tok.iterator(sentit.next());

				// get the tokens and words
				while (tokit.hasNext()) {
					Token t = tokit.next();
					words.add(t.getCoveredText());
					tokens.add(t);
				}
			}

			tt.process(words);

			// add the lemmas and tags to the tokens
			for (int i = 0; i < tokens.size(); i++) {
				Token aToken = tokens.get(i);
				if (i < tags.size()) {
					aToken.setTag(tags.get(i));
				}
				if (i < lemmas.size()) {
					if (lemmas.get(i) != null) {
						aToken.setLemma(lemmas.get(i).toLowerCase());
					}
				}
			}

			tags.clear();
			lemmas.clear();
			tokens.clear();

		} catch (Exception e) {
			throw new AnalysisEngineProcessException(e);
		}
	}
}
