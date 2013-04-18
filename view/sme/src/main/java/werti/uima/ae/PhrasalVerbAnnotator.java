package werti.uima.ae;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Set;

import org.apache.log4j.Logger;
import org.apache.uima.UimaContext;
import org.apache.uima.analysis_component.JCasAnnotator_ImplBase;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.cas.text.AnnotationIndex;
import org.apache.uima.jcas.JCas;
import org.apache.uima.jcas.cas.FSArray;
import org.apache.uima.resource.ResourceInitializationException;
import werti.uima.types.annot.PhrasalVerb;
import werti.uima.types.annot.SentenceAnnotation;
import werti.uima.types.annot.Token;

/**
 * The phrasal verb annotator adapted from Tatiana Vodolazova's python implementation.
 * 
 * @author Adriane Boyd
 * @version 0.1
 */
public class PhrasalVerbAnnotator extends JCasAnnotator_ImplBase {
	private static final Logger log =
		Logger.getLogger(PhrasalVerbAnnotator.class);
	
	private HashMap<String, Set<String>> insepList;
	private HashMap<String, Set<String>> intransList;
	private HashMap<String, Set<String>> sepList;
	private HashMap<String, Set<String>> sepobligList;
	
	// the verb and particle lists are also used by the PhrasalVerbFilter
	public static Set<String> verbList;
	public static Set<String> particleList;
		
	private static final String verbPOSRegex = "VB|VBD|VBG|VBN|VBP|VBZ";
	private static final int maxParticleLength = 3;
	private static final int maxInterveningTokens = 5;

	public void initialize(UimaContext context) throws ResourceInitializationException {
		super.initialize(context);
	
		String insep =  (String) context.getConfigParameterValue("inseparableFileLocation");
		String intrans =  (String) context.getConfigParameterValue("intransitiveFileLocation");
		String sep =  (String) context.getConfigParameterValue("separableFileLocation");
		String sepoblig =  (String) context.getConfigParameterValue("separable_obligFileLocation");
		
		insepList = readVerbList(insep);
		intransList = readVerbList(intrans);
		sepList = readVerbList(sep);
		sepobligList = readVerbList(sepoblig);
		
		verbList = new HashSet<String>();
		verbList.addAll(insepList.keySet());
		verbList.addAll(intransList.keySet());
		verbList.addAll(sepList.keySet());
		verbList.addAll(sepobligList.keySet());
		
		particleList = new HashSet<String>();
		particleList.addAll(makeParticleList(insepList));
		particleList.addAll(makeParticleList(intransList));
		particleList.addAll(makeParticleList(sepList));
		particleList.addAll(makeParticleList(sepobligList));
	}

	@SuppressWarnings("unchecked")
	public void process(JCas cas) throws AnalysisEngineProcessException {
		log.debug("Starting phrasal verb annotation");
		
		final AnnotationIndex sentIndex = cas.getAnnotationIndex(SentenceAnnotation.type);
		final AnnotationIndex tokenIndex = cas.getAnnotationIndex(Token.type);
		final Iterator<SentenceAnnotation> sit = sentIndex.iterator();
		
		while (sit.hasNext()) {
			final Iterator<Token> tit = tokenIndex.subiterator(sit.next());
			
			List<Token> tokenlist = new ArrayList<Token>();
			
			// get a list of tokens
			int i = 0;
			while (tit.hasNext()) {
				Token t = tit.next();
				
				// create a list of tokens
				tokenlist.add(t);
				
				i++;
			}
			
			Token mostRecentVerb = null;
			i = 0;
			List<Token> intTokens = new ArrayList<Token>();
			
			for (i = 0; i < tokenlist.size(); i++) {
				// don't allow more than a certain number of intervening tokens
				if (intTokens.size() >= maxInterveningTokens) {
					mostRecentVerb = null;
					intTokens.clear();
				}
				
				Token t = tokenlist.get(i);
				// keep track of intervening tokens
				intTokens.add(t);
				
				// keep track of the last verb we've seen,
				// start a new list of intervening tokens
				if (t.getTag().matches(verbPOSRegex)) {
					mostRecentVerb = t;
					intTokens.clear();
				}
				
				// if we have found a recent verb and we're at least one token beyond the most recent verb
				if (mostRecentVerb != null && !t.getTag().matches(verbPOSRegex)) {
					// look for particles in the next 1/2/3 tokens
					List<Token> mostRecentParticleList = new ArrayList<Token>();
					for (int j = i; j < i + maxParticleLength && j < tokenlist.size(); j++) {
						mostRecentParticleList.add(tokenlist.get(j));
					}
					
					// generate possible particles with the next 1/2/3 words
					List<String> possibleParticles = new ArrayList<String>();
					for (int j = i; j < i + maxParticleLength && j < tokenlist.size(); j++) {
						possibleParticles.add(j - i, "");
					}
					
					for (int j = 0; j < mostRecentParticleList.size(); j++) {
						String text = mostRecentParticleList.get(j).getCoveredText().toLowerCase();
						for (int k = j; k < possibleParticles.size(); k++) {
							String extendedParticle = possibleParticles.get(k) + " " + text;
							possibleParticles.set(k, extendedParticle.trim());
						}
					}
								
					boolean checkLists = false;
					for (String particle: possibleParticles) {
						if (particleList.contains(particle)) {
							checkLists = true;
						}
					}
					
					if (checkLists) {						
						// remove the current token from the intervening token list
						intTokens.remove(intTokens.size() - 1);
						Token nextToken = null;
						if (i+1 < tokenlist.size()) {
							nextToken = tokenlist.get(i+1);
						}
						
						// figure out which, if any, longest possible particle is in one of the lists
						int found = -1;
						for (int j = possibleParticles.size() - 1; j >= 0; j--) {
							if (found < 0 && inPhrasalVerbList(mostRecentVerb, possibleParticles.get(j), intTokens, nextToken)) {
								found = j;
							}
						}
						
						// if a phrasal verb was found, add to annotation
						if (found >= 0) {
							PhrasalVerb pverb = new PhrasalVerb(cas);
							
							// copy the particle(s) into an FSArray
							
							// figure out the particle length based on maxParticleLength and found index
							int plSize = found + 1;

							final FSArray particle = new FSArray(cas, plSize);
							Token[] particles = new Token[plSize];
							for(int j = i; j < i + plSize; j++) {
								particles[j - i] = tokenlist.get(j);
							}
							Token lastToken = particles[particles.length - 1];
							particle.copyFromArray(particles, 0, 0, particles.length);
							
							// copy the verb into an FSArray
							final FSArray verb = new FSArray(cas, 1);
							Token[] verbs = new Token[1];
							verbs[0] = mostRecentVerb;
							verb.copyFromArray(verbs, 0, 0, 1);
							
							// generate the annotation
							pverb.setParticle(particle);
							pverb.setVerb(verb);
							pverb.setBegin(mostRecentVerb.getBegin());
							pverb.setEnd(lastToken.getEnd());
							pverb.addToIndexes();
							
							mostRecentVerb = null;
						}
						
						// add the particle back to the intervening tokens list
						intTokens.add(t);
					}
				}
			}
		}

		log.debug("Finished phrasal verb annotation");
	}

	/**
	 * Read in file containings lists of verbs with their particles.
	 * 
	 * @param file	file name
	 * @return Hash of verb lemmas with sets of (potentially multi-token) particles
	 * @throws ResourceInitializationException
	 */
	private HashMap<String, Set<String>> readVerbList(String file) throws ResourceInitializationException {
		HashMap<String, Set<String>> verbList = new HashMap<String, Set<String>>();

		try {
			BufferedReader input =  new BufferedReader(new FileReader(file));

			String line;

			while ((line = input.readLine()) != null) {
				String[] lineParts = line.split(":");
				String verb = lineParts[0];
				String[] particleParts = lineParts[1].split(",");
				Set<String> particles = new HashSet<String>();
				for(int i = 0; i < particleParts.length; i++) {
					particles.add(particleParts[i]);
				}
				verbList.put(verb, particles);
			}
		} catch (FileNotFoundException e) {
			throw new ResourceInitializationException(e);
		} catch (IOException e) {
			throw new ResourceInitializationException(e);
		}
		
		return verbList;
	}

	/**
	 * Extract a list of all possible particles from a verb/particle hash.
	 * 
	 * @param verbList
	 * @return
	 */
	private Set<String> makeParticleList(HashMap<String, Set<String>> verbList) {
		Set<String> particleList = new HashSet<String>();
		
		Set<String> verbs = verbList.keySet();
		for (String verb : verbs) {
			for (String particle : verbList.get(verb)) {
				particleList.add(particle);
			}
		}
		
		return particleList;
	}
	
	/**
	 * Check if a potential verb/particle combination is found in any of the
	 * verb/particle lists.
	 * 
	 * @param mostRecentVerb
	 * @param particle
	 * @param intTokens
	 * @param nextToken
	 * @return
	 */
	private boolean inPhrasalVerbList(Token mostRecentVerb, String particle, List<Token> intTokens, Token nextToken) {	
		String mostRecentVerbBaseform = mostRecentVerb.getLemma();
		
		// check inseparable cases
		if (insepList.containsKey(mostRecentVerbBaseform)) {
			if (insepList.get(mostRecentVerbBaseform).contains(particle)) {
				// if there are no intervening tokens
				if (intTokens.size() == 0) {
					return true;
				}
			}
		}
		
		// check intransitive cases
		if (intransList.containsKey(mostRecentVerbBaseform)) {
			if (intransList.get(mostRecentVerbBaseform).contains(particle)) {
				// if the next phrase isn't an NP (very rough check)
				if (nextToken != null && nextToken.getChunk() != "B-NP") {
					return true;
				}
			}
		} 
		
		// check if a new clause starts in the intervening tokens
		// if so, don't consider this is as a separable case
		for(Token t : intTokens) {
			if (t.getChunk() == "B-SBAR") {
				return false;
			}
		}

		// check separable cases
		if (sepList.containsKey(mostRecentVerbBaseform)) {
			if (sepList.get(mostRecentVerbBaseform).contains(particle)) {
				return true;
			}
		}
		
		// check obligatory separable cases
		if (sepobligList.containsKey(mostRecentVerbBaseform)) {
			if (sepobligList.get(mostRecentVerbBaseform).contains(particle)) {
				// if there are some intervening tokens
				if (intTokens.size() > 0) {
					// check if there is an intervening NP
					for (int i = 0; i < intTokens.size(); i++) {
						Token t = intTokens.get(i);
						if (t.getChunk() == "B-NP") {
							return true;
						}
					}
				}
			}
		}
		
		return false;
	}
}
