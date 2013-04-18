package werti.uima.enhancer;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Stack;

import org.apache.log4j.Logger;
import org.apache.uima.UimaContext;
import org.apache.uima.analysis_component.JCasAnnotator_ImplBase;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.cas.FSIterator;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceInitializationException;
import werti.uima.types.Enhancement;
import werti.uima.types.annot.CGReading;
import werti.uima.types.annot.CGToken;
import werti.util.EnhancerUtils;
import werti.util.StringListIterable;

/**
 * Use the TAG-B TAG-I sequences resulting from the CG3 analysis with
 * {@link werti.ae.Vislcg3Annotator} to enhance spans corresponding 
 * to the tags specified by the activity as conjunction tags.
 * 
 * @author Niels Ott?
 * @author Adriane Boyd
 * @author Heli Uibo
 *
 */
public class Vislcg3ConjunctionEnhancer extends JCasAnnotator_ImplBase {

	private static final Logger log =
		Logger.getLogger(Vislcg3ConjunctionEnhancer.class);
	
	private List<String> conjunctionTags;
	private static String CHUNK_BEGIN_SUFFIX = "-B";
	private static String CHUNK_INSIDE_SUFFIX = "-I";
	
	@Override
	public void initialize(UimaContext context)
			throws ResourceInitializationException {
        log.debug("Conjunction tags "+conjunctionTags);
		super.initialize(context);
		conjunctionTags = Arrays.asList(((String)context.getConfigParameterValue("conjunctionTags")).split(","));
	}

	@Override
	public void process(JCas cas) throws AnalysisEngineProcessException {
		log.info("Starting conjunction enhancement");
		// stack for started enhancements (chunk)
		// Stack<Enhancement> enhancements = new Stack<Enhancement>();
		// keep track of ids for each annotation class
		HashMap<String, Integer> classCounts = new HashMap<String, Integer>();
		for (String conT : conjunctionTags) {
			classCounts.put(conT, 0);
			log.info("Tag: "+conT);
		}

		// iterating over chunkTags instead of classCounts.keySet() because it is important to control the order in which
		// spans are enhanced
		
		for (String conT: conjunctionTags) {
			FSIterator cgTokenIter = cas.getAnnotationIndex(CGToken.type).iterator();
			// remember previous token so we can getEnd() from it (chunk)
			// CGToken prev = null;
			int newId = 0;
			// go through tokens
			while (cgTokenIter.hasNext()) {
				CGToken cgt = (CGToken) cgTokenIter.next();
				// more than one reading? don't mark up!
				if (!isSafe(cgt)) {
					continue;
				}

				// analyze reading
				CGReading reading = cgt.getReadings(0);
				//log.info("next reading: "+reading);
				/*
				// annotation of each token individually
				if (containsTag(reading, conT)) {
					Enhancement e = new Enhancement(cas);
					
					// determine token position within chunk
					String tokenPosition = CHUNK_BEGIN_SUFFIX;
					if (containsTag(reading, conT + CHUNK_INSIDE_SUFFIX)) {
						tokenPosition = CHUNK_INSIDE_SUFFIX;
					}
					// increment id
					int newId = classCounts.get(conT) + 1;
					classCounts.put(conT, newId);
					
					e.setBegin(cgt.getBegin());
					e.setEnhanceStart("<span id=\"" + EnhancerUtils.get_id("WERTi-span-" + conT, newId) + 
							"\" class=\"wertiviewconjunction wertiview" + conT + " werti" + conT + tokenPosition + "\">");
					e.setEnd(cgt.getEnd());
					e.setEnhanceEnd("</span>");
					
					cas.addFsToIndexes(e);
				} 
				*/
				
				/* annotation of spans across tokens */	
				/*			 
				// case 1: started enhancement but current reading doesn't
				// have a chunk inside tag					
                    if (!enhancements.empty() && enhancements.peek().getEnhanceStart().contains(conT)
								&& !containsTag(reading, conT)) {
					// finish enhancement
					Enhancement e = enhancements.pop();
					e.setEnd(prev.getEnd());
					e.setEnhanceEnd("</span>");
					e.setRelevant(true);
					// update CAS
					cas.addFsToIndexes(e);
					log.debug("Completed chunk " + conT + "-" + classCounts.get(conT) + " at pos " + e.getEnd());
				}
				*/
				
				// case 2: chunk start tag
				if (containsTag(reading, conT)) {
					// make new enhancement
					Enhancement e = new Enhancement(cas);
					e.setRelevant(true);
					e.setBegin(cgt.getBegin());
					e.setEnd(cgt.getEnd());
					
					// increment id
					newId = classCounts.get(conT) + 1;
					e.setEnhanceStart("<span id=\"" + EnhancerUtils.get_id("WERTi-span-" + conT, newId) + "\" class=\"wertiviewtoken wertiviewconjunction wertiview" + conT + "\">");					
					e.setEnhanceEnd("</span>");
					classCounts.put(conT, newId);
					//log.info(newId);
					// push onto stack
					//enhancements.push(e);
					// update CAS
					cas.addFsToIndexes(e);
					//e.addToIndexes();
					//log.info("Started conjunction " + conT + "-" + newId + " at pos " + e.getBegin());
				}

				//prev = cgt;
			}
		}
		

		// (chunk)
		//log.info("Enhancement stack is "
		//		+ (enhancements.empty() ? "empty, OK" : "not empty, WTF??"));
		log.info("Finished conjunction enhancement");
	}
	
	/*
	 * Determines whether the given token is safe, i.e. unambiguous
	 */
	private boolean isSafe(CGToken t) {
		return t.getReadings() != null && t.getReadings().size() == 1;
	}
	
	/*
	 * Determines whether the given reading contains the given tag
	 */
	private boolean containsTag(CGReading cgr, String tag) {
		StringListIterable reading = new StringListIterable(cgr);
		for (String rtag : reading) {
			if (tag.equals(rtag)) {
			    //log.info(cgr + " contains " + tag);
				return true;
			}
		}
		//log.info(cgr + " does not contain " + tag);
		return false;
	}

}
