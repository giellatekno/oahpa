package werti.server;

import java.io.IOException;
import java.net.URL;
import java.util.Properties;
import java.util.Set;
import java.util.TreeMap;

import javax.servlet.ServletException;

import org.apache.log4j.Logger;
import org.apache.uima.UIMAFramework;
import org.apache.uima.analysis_engine.AnalysisEngine;
import org.apache.uima.analysis_engine.AnalysisEngineDescription;
import org.apache.uima.resource.ResourceInitializationException;
import org.apache.uima.resource.metadata.ConfigurationParameterSettings;
import org.apache.uima.util.InvalidXMLException;
import org.apache.uima.util.XMLInputSource;

/**
 * Stores an instance of each the pre- and postprocessors for each topic
 * so that the model files only need to be loaded once.  (Note: Doesn't 
 * actually work like I intended, will be replaced with Aleks' WERTiContext
 * in the near future.)
 * 
 * @author Adriane Boyd
 */
public class Processors {
	private static final Logger log =
		Logger.getLogger(Processors.class);

	private TreeMap<String, TreeMap<String, AnalysisEngine>> preMap;
	private TreeMap<String, TreeMap<String, AnalysisEngine>> postMap;
    
	public Processors(Activities activities) throws IOException, ServletException {
		preMap = new TreeMap<String, TreeMap<String, AnalysisEngine>>();
		postMap = new TreeMap<String, TreeMap<String, AnalysisEngine>>();
		
		for (String activity : activities) {
			ActivityConfiguration config = activities.getActivity(activity);
			log.info("Config:"+config);
			//log.info("Activity:"+activity);
			
			Set<String> langs = config.getLanguages();
			
			for (String l : langs) {
				if (!preMap.containsKey(l)) {
					preMap.put(l, new TreeMap<String, AnalysisEngine>());
				}
				if (!postMap.containsKey(l)) {
					postMap.put(l, new TreeMap<String, AnalysisEngine>());
				}
				
				final URL preDesc, postDesc;
				preDesc = config.getPreDesc(l);
				postDesc = config.getPostDesc(l);
				log.info("Preprocess descriptor "+preDesc);
				log.info("Postprocess descriptor"+postDesc);

				try { // to initialize UIMA components
					preMap.get(l).put(activity, initAE(loadDescriptor(preDesc), config.getServerPreConfigAsProp(l)));
					postMap.get(l).put(activity, initAE(loadDescriptor(postDesc), config.getServerPostConfigAsProp(l)));
				} catch (InvalidXMLException ixmle) {
					log.fatal("Error initializing XML code. Invalid?", ixmle);
					throw new ServletException("", ixmle);
				} catch (ResourceInitializationException rie) {
					log.fatal("Error initializing resource", rie);
					throw new ServletException("", rie);
				} catch (IOException ioe) {
					log.fatal("Error accessing descriptor file", ioe);
					throw new ServletException("", ioe);
				} catch (NullPointerException npe) {
					log.fatal("Error accessing descriptor files or creating analysis objects", npe);
					throw new ServletException("", npe);
				}
			}
		}	
	}
	
	public AnalysisEngine getPreprocessor(String lang, String key) {
		if (preMap.containsKey(lang)) {
			return preMap.get(lang).get(key);
		}
		
		return null;
	}
	
	public AnalysisEngine getPostprocessor(String lang, String key) {
		if (postMap.containsKey(lang)) {
			return postMap.get(lang).get(key);
		}
		
		return null;
	}	
	
	/**
	 * Private helper that auto-converts a string to another type, depending on 
	 * a given type. The fallback strategy is to produce a clone of the string passed to
	 * the method.
	 * @param originalParameter the given type that determines the return type
	 * @param value the value to convert into the new type
	 * @return an object of the same type as originalParameter holding the parsed value.
	 * @throws NumberFormatException if the parsing went wrong.
	 */
	private Object autoConvertParameter(Object originalParameter, String value) {
		
		if ( originalParameter instanceof Boolean) {
			return Boolean.parseBoolean(value);
		}
		if ( originalParameter instanceof Integer) {
			return Integer.parseInt(value);
		}
		if ( originalParameter instanceof Float) {
			return Float.parseFloat(value);
		}
		
		// fallback: return as string
		return new String(value);
		
	}	
	
	/**
	 * Private helper that creates an object holding an analysis engine description from file.
	 * @param descriptor the path to the analysis engine descriptor file.
	 * @return an object holding the AE description.
	 * @throws IOException
	 * @throws InvalidXMLException
	 */
	private AnalysisEngineDescription loadDescriptor(URL descriptor) throws IOException, InvalidXMLException {

		log.debug("Loading AE descriptor from url:  " + descriptor.getPath());
		XMLInputSource xmlInput = new XMLInputSource(descriptor);
		AnalysisEngineDescription description = UIMAFramework.getXMLParser().parseAnalysisEngineDescription(xmlInput);
		return description;
		
	}
	
	/**
	 * Private helper initializing the UIMA pipeline.
	 * @throws ResourceInitializationException
	 */
	private AnalysisEngine initAE(AnalysisEngineDescription description, Properties config) throws ResourceInitializationException {

		// read descriptor from disk and initialize a new annotator
		// adjust configuration in the AE description by setting all parameters from config
		ConfigurationParameterSettings settings = description.getAnalysisEngineMetaData().getConfigurationParameterSettings(); 
		for ( Object k : config.keySet() ) {
			String key = (String)k;
			String value = (String)config.get(key);
			
			// auto-adjust type of the parameter according to the type found in the description
			Object genericTypeValue = autoConvertParameter(settings.getParameterValue(key), value);
			settings.setParameterValue(key, genericTypeValue);
			
			log.debug("Setting AE parameter: " + key + "=" + value);
		}
		
		// produce the annotator from the description
		log.debug("Initializing AE.");
		return UIMAFramework.produceAnalysisEngine(description);
		
	}
}
