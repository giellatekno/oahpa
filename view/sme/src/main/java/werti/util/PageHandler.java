package werti.util;

import javax.servlet.ServletException;

import org.apache.log4j.Logger;
import org.apache.uima.analysis_engine.AnalysisEngine;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceInitializationException;
import werti.server.Processors;

/**
 * Methods needed for processing a document regardless of whether it came
 * from the web form or from the add-on.
 * 
 * @author Adriane Boyd
 *
 */
public class PageHandler {
	private static final Logger log =
		Logger.getLogger(PageHandler.class);
	
	Processors processors;
	String topic;
	String text;
	String lang;
	
	public PageHandler(Processors aProcessors, String aTopic, String aText, String aLang) {
		processors = aProcessors;
		topic = aTopic;
		text = aText;
		lang = aLang;
		/*if (topic.compareTo("Conjunctions") == 0){
			lang = "sme";
		}
		log.info(processors+" "+topic+" "+lang);*/
	}

	/**
	 * Creates a CAS from the text and runs the pre- and postprocessors for the
	 * topic.
	 * 
	 * @return CAS containing annotation
	 * @throws ServletException
	 */
	public JCas process() throws ServletException {
		AnalysisEngine preprocessor = processors.getPreprocessor(lang, topic);
		AnalysisEngine postprocessor = processors.getPostprocessor(lang, topic);
		if (preprocessor != null && postprocessor != null) {
			try { // to process
				JCas cas = preprocessor.newJCas();
				cas.setDocumentText(text);
				cas.setDocumentLanguage(lang);
				preprocessor.process(cas);
				postprocessor.process(cas);
				return cas;
			} catch (AnalysisEngineProcessException aepe) {
				log.fatal("Analysis Engine encountered errors!", aepe);
				throw new ServletException("Text analysis failed.", aepe);
			} catch (ResourceInitializationException rie) {
				log.fatal("Resource Initialization Engine encountered errors!", rie);
				throw new ServletException("Text analysis failed.", rie);
			}
		}
		
		return null;
	}
}
