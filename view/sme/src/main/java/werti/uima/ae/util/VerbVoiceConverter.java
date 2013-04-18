package werti.uima.ae.util;

import java.util.ArrayList;
import java.util.List;

import org.apache.log4j.Logger;

import org.apache.uima.analysis_engine.AnalysisEngineProcessException;

import werti.uima.types.annot.Token;

/**
 * Convert verbs between active and passive voice, keeping track of
 * intervening adverbs.
 * 
 * @author Adriane Boyd
 *
 */
public class VerbVoiceConverter {
	private static final Logger log =
		Logger.getLogger(VerbVoiceConverter.class);

	private Morphg mg;

	public VerbVoiceConverter(Morphg amg) {
		mg = amg;
	}

	public String activeToPassive(Token subj, List<Token> verb) throws AnalysisEngineProcessException {
		List<Token> tensed = new ArrayList<Token>();
		List<Token> adverbs = new ArrayList<Token>();
		List<Token> untensed = new ArrayList<Token>();
				
		for (int i = 0; i < verb.size(); i++) {
			if (i == 0) {
				tensed.add(verb.get(i));
			} else {
				if (!verb.get(i).getTag().matches("^(V|MD).*")) {
					adverbs.add(verb.get(i));
				} else {
					untensed.add(verb.get(i));
				}
			}
		}
		
		// if we don't have a tensed verb, abort
		if (tensed.size() == 0) {
			return "";
		}
		
		String mainVerb = "";
		if (untensed.size() == 0) {
			mainVerb = tensed.get(0).getLemma().toLowerCase();
		} else {
			mainVerb = untensed.get(untensed.size() - 1).getLemma().toLowerCase();
		}
		
		// get all the relevant verb forms to make tense detection easier
		String input = mainVerb + "+ing_VBG" + "\t" + mainVerb + "+ed_VBD" + "\t" + mainVerb + "+en_VBN";
		String output = mg.process(input);
		String[] outputParts = output.split("\\t");
		String baseVerb = mainVerb;
		String gerundVerb = outputParts[0];
		String pastVerb = outputParts[1];
		String ppVerb = outputParts[2];

		/* important tense distinctions, that depend on the form of the
		 * main verb and the length of the verb list
		 * 
		 *   pres		present				find
		 *   cont		continuous			is/was/has been finding
		 *   past		past				found
		 *   perf		perfect				(will)? have/had found
		 *   modal		future/modal		will/can find
		 */
		String tense = "";
		boolean doSupport = false;
		
		if (untensed.size() == 0) { // one main verb
			if (tensed.get(0).getCoveredText().matches("(?i)" + pastVerb)) {
				tense = "past";
			} else {
				tense = "pres";
			}
		} else { // multiple verbs
			// check for "do", which will be removed in the passive by
			// treating the main verb as a single form
			if (tensed.get(0).getLemma().equals("do")) {
				doSupport = true;
				if (tensed.get(0).getCoveredText().matches("(?i)do(es)?")) {
					tense = "pres";
				} else {
					tense = "past";
				}
			} else {
				Token t = untensed.get(untensed.size() - 1);
				if (t.getCoveredText().matches("(?i)" + baseVerb)) {
					tense = "modal";
				} else if (t.getCoveredText().matches("(?i)" + ppVerb)) {
					tense = "perf";
				} else if (t.getCoveredText().matches("(?i)" + gerundVerb)) {
					tense = "cont";
				}
			}
		}

		String finalTensed = "";
		String finalUntensed = "";
		String agr = getNPAgr(subj);
		
		if (tense.equals("pres") || tense.equals("past")) {	
			if (tense.equals("pres")) {
				if (agr.equals("1s")) {
					finalTensed = "am";
				} else if (agr.equals("3s")) {
					finalTensed = "is";
				} else {
					finalTensed = "are";
				}
			} else {
				if (agr.equals("1s") || agr.equals("3s")) {
					finalTensed = "was";
				} else {
					finalTensed = "were";
				}
			}

			if (doSupport) {
				finalUntensed = ppVerb;
			} else {
				finalTensed += " " + ppVerb;
			}
		} else {
			// otherwise, we can leave the tensed verb as is (except for person/number)
			// and just worry adding "be" to the untensed list
			finalTensed = tensed.get(0).getCoveredText();
			String adjustedAux = adjustAuxVerbAgr(finalTensed, agr);
			
			if (!adjustedAux.equals("")) {
				finalTensed = adjustedAux;
			}
					
			for (int i = 0; i < untensed.size() - 1; i++) {
				finalUntensed += untensed.get(i).getCoveredText() + " ";
			}
			
			if (tense.equals("cont")) {
				finalUntensed += "being " + ppVerb;
			} else if (tense.equals("perf")) {
				finalUntensed += "been " + ppVerb;
			} else if (tense.equals("modal")) {
				finalUntensed += "be " + ppVerb;
			}
		}
	
		String finalAdverbs = "";
		for (Token t : adverbs) {
			finalAdverbs += t.getCoveredText() + " ";
		}
		finalAdverbs = finalAdverbs.trim();
		
		String convertedVerb = finalTensed + " " + finalAdverbs + " " + finalUntensed;
		convertedVerb = convertedVerb.replaceAll(" N'T", "N'T");
		convertedVerb = convertedVerb.replaceAll("(?i) n't", "n't");
		convertedVerb = convertedVerb.replaceAll("\\s+", " ");
		
		return convertedVerb;
	}
	
	public String passiveToActive(Token subj, List<Token> verb) throws AnalysisEngineProcessException {
		if (log.isDebugEnabled()) {
			final StringBuffer subS = new StringBuffer();
			final StringBuffer vrbS = new StringBuffer();
			subS.append(subj.getCoveredText()+" ");
			for (final Token t:verb) { vrbS.append(t.getCoveredText()+" "); }
			log.debug("Subj is "+subS+"; Verb is "+vrbS);
		}
		List<Token> tensed = new ArrayList<Token>();
		List<Token> adverbs = new ArrayList<Token>();
		List<Token> untensed = new ArrayList<Token>();
				
		for (int i = 0; i < verb.size(); i++) {
			if (i == 0) {
				tensed.add(verb.get(i));
			} else {
				if (!verb.get(i).getTag().matches("^(V|MD).*")) {
					adverbs.add(verb.get(i));
				} else {
					untensed.add(verb.get(i));
				}
			}
		}
		
		// all passives involve at least two tokens in the verb form,
		// if we don't have at least two tokens, abort
		if (tensed.size() == 0 || untensed.size() < 1) {
			return "";
		}
		
		String mainVerb = untensed.get(untensed.size() - 1).getLemma().toLowerCase();
		
		// get all the relevant verb forms
		String input = mainVerb + "+s_VBZ" + "\t" + mainVerb + "+ing_VBG" + "\t" + mainVerb + "+ed_VBD";
		String output = mg.process(input);
		String[] outputParts = output.split("\\t");
		String pres3sVerb = outputParts[0];
		String gerundVerb = outputParts[1];
		String pastVerb = outputParts[2];
		
		/* important tense distinctions, that depend on the form of "be"
		 * immediately preceding the past participle
		 * 
		 *   pres		present				is found
		 *   cont		continuous			is/was/has been/etc. being found
		 *   past		past				was found
		 *   perf		perfect				(will)? have/had been found
		 *   modal		future/modal		will/can be found
		 */
		String tense = "";
		if (tensed.size() + untensed.size() == 2) {
			if (tensed.get(0).getCoveredText().matches("(?i)(was|were)")) {
				tense = "past";
			} else {
				tense = "pres";
			}
		} else {
			for (int i = untensed.size() - 1; i >= 0; i--) {
				Token t = untensed.get(i);
				if (t.getLemma().matches("(?i)be")) {
					if (t.getCoveredText().matches("(?i)be")) {
						tense = "modal";
					} else if (t.getCoveredText().matches("(?i)been")) {
						tense = "perf";
					} else if (t.getCoveredText().matches("(?i)being")) {
						tense = "cont";
					}
				}
			}
		}

		String finalTensed = "";
		String finalUntensed = "";
		String agr = getNPAgr(subj);
		
		if (tense.equals("pres") || tense.equals("past")) {	
			if (tense.equals("pres")) {
				if (agr.equals("3s")) {
					finalTensed = pres3sVerb;
				} else {
					finalTensed = untensed.get(0).getLemma();
				}
			} else {
				finalTensed = pastVerb;
			}
		} else {
			// otherwise, we can leave the tensed verb as is (except for person/number)
			// and just worry about removing "be" from the untensed list
			finalTensed = tensed.get(0).getCoveredText();
			String adjustedAux = adjustAuxVerbAgr(finalTensed, agr);

			if (!adjustedAux.equals("")) {
				finalTensed = adjustedAux;
			}
			
			for (int i = 0; i < untensed.size() - 2; i++) {
				finalUntensed += untensed.get(i).getCoveredText() + " ";
			}
			
			if (tense.equals("cont")) {
				finalUntensed += gerundVerb;
			} else if (tense.equals("perf")) {
				finalUntensed += untensed.get(untensed.size() - 1).getCoveredText();
			} else if (tense.equals("modal")) {
				finalUntensed += untensed.get(untensed.size() - 1).getLemma();
			}
		}
		
		String finalAdverbs = "";
		for (Token t : adverbs) {
			finalAdverbs += t.getCoveredText() + " ";
		}
		finalAdverbs = finalAdverbs.trim();
		
		String convertedVerb = finalTensed + " " + finalAdverbs + " " + finalUntensed;
		convertedVerb = convertedVerb.replaceAll(" N'T", "N'T");
		convertedVerb = convertedVerb.replaceAll("(?i) n't", "n't");
		convertedVerb = convertedVerb.replaceAll("\\s+", " ");
		
		return convertedVerb;
	}
	
	/**
	 * A quick analysis of the person/number of an NP.
	 * 
	 * @param np
	 * @return abbreviated string (e.g., "1s", "2p") representing the person/number
	 */
	private String getNPAgr(Token noun) {
		String tag = noun.getTag();
		if (tag.matches("(NN|NN?P)")) {
			return "3s";
		} else if (tag.matches("(NNS|NN?PS)")) {
			return "3p";
		}
		
		if (tag.matches("PRP")) {
			String pro = noun.getCoveredText().toLowerCase();
			
			if (pro.equals("I") || pro.equals("me")) {
				return "1s";			
			} else if (pro.equals("you")) {
				return "2s";
			} else if (pro.equals("he") || pro.equals("she") || pro.equals("him") || pro.equals("her") || pro.equals("it")) {
				return "3s";
			} else if (pro.equals("we") || pro.equals("us")) {
				return "1p";
			} else if (pro.equals("they") || pro.equals("them")) {
				return "3p";
			}
		}
		
		return "";
	}

	/**
	 * Given person/number of subject, adjust person/number of 
	 * auxiliary verbs.
	 * 
	 * @param tensedText
	 * @param agr
	 * @return
	 */
	private String adjustAuxVerbAgr(String tensedText, String agr) {
		String finalTensed = "";

		if (tensedText.matches("(?i)(has|have)")) {
			if (agr.equals("3s")) {
				finalTensed = "has";
			} else {
				finalTensed = "have";
			}
		} else if (tensedText.matches("(?i)(am|are|is)")) {
			if (agr.equals("1s")) {
				finalTensed = "am";
			} else if (agr.equals("3s")) {
				finalTensed = "is";
			} else {
				finalTensed = "are";
			}
		} else if (tensedText.matches("(?i)(was|were)")) {
			if (agr.equals("1s") || agr.equals("3s")) {
				finalTensed = "was";
			} else {
				finalTensed = "were";
			}
		}

		return finalTensed;
	}
}
