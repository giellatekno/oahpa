package werti.uima.ae;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.SortedSet;

import org.apache.log4j.Logger;
import org.apache.uima.UimaContext;
import org.apache.uima.analysis_component.JCasAnnotator_ImplBase;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.cas.text.AnnotationIndex;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceInitializationException;
import org.maltparser.MaltParserService;
import org.maltparser.core.exception.MaltChainedException;
import org.maltparser.core.symbol.SymbolTable;
import org.maltparser.core.syntaxgraph.DependencyStructure;
import org.maltparser.core.syntaxgraph.node.DependencyNode;

import werti.WERTiContext;
import werti.WERTiContext.WERTiContextException;
import werti.uima.types.annot.SentenceAnnotation;
import werti.uima.types.annot.Token;

/**
 * Portions of this annotator were adapted from cleartk:
 * 
 * Copyright (c) 2010, Regents of the University of Colorado <br>
 * All rights reserved.
 */
public class MaltParser extends JCasAnnotator_ImplBase {
	private static final Logger log =
		Logger.getLogger(MaltParser.class);

	private static Map<String, MaltParserService> parsers;
	
	@Override
	public void initialize(UimaContext aContext)
			throws ResourceInitializationException {
		super.initialize(aContext);
		
		try {
			parsers = new HashMap<String, MaltParserService>();
			//parsers.put("en", WERTiContext.request(MaltParserService.class, "en"));
			parsers.put("de", WERTiContext.request(MaltParserService.class, "de"));
		} catch (WERTiContextException wce) {
			throw new ResourceInitializationException(wce);
		}
	}

	@SuppressWarnings("unchecked")
	@Override
	public void process(JCas jcas) throws AnalysisEngineProcessException {
		log.debug("Starting malt parser annotation");
		
		final String lang = jcas.getDocumentLanguage();
		
		MaltParserService parser;
		
		if (parsers.containsKey(lang)) {
			parser = parsers.get(lang);
		} else {
			log.error("No MaltParser for language: " + lang);
			throw new AnalysisEngineProcessException();
		}

		final AnnotationIndex sentIndex = jcas.getAnnotationIndex(SentenceAnnotation.type);
		final AnnotationIndex tokenIndex = jcas.getAnnotationIndex(Token.type);

		final Iterator<SentenceAnnotation> sit = sentIndex.iterator();
		
		while (sit.hasNext()) {
			SentenceAnnotation s = sit.next();

			final Iterator<Token> tit = tokenIndex.subiterator(s);

			List<String> inputStrings = new ArrayList<String>();
			List<Token> tokens = new ArrayList<Token>();

			// line format is <index>\t<word>\t_\t<pos>\t<pos>\t_		
			final String lineFormat = "%1$d\t%2$s\t_\t%3$s\t%3$s\t_";
			
			int lineNo = 1;
			
			while (tit.hasNext()) {
				// keep a list of tokens to refer to when inserting
				// the parse into the CAS
				Token t = tit.next();
				tokens.add(t);
				
				String text = t.getCoveredText();
				String pos = t.getTag();
	
				inputStrings.add(String.format(lineFormat, lineNo, text, pos));
				lineNo += 1;
			}
			
			// skip parsing for sentences without tokens because MaltParser crashes
			if (tokens.size() == 0) {
				continue;
			}

			try {
				// parse with MaltParser
				String[] input = inputStrings.toArray(new String[inputStrings.size()]);
				DependencyStructure graph = parser.parse(input);
				
				SortedSet<Integer> tokenIndices = graph.getTokenIndices();

				// add head links between node annotations
				SymbolTable table = (SymbolTable) graph.getSymbolTables().getSymbolTable("DEPREL");
				for (int i : tokenIndices) {
					DependencyNode maltNode = graph.getTokenNode(i);
					int headIndex = maltNode.getHead().getIndex();
					Token t = tokens.get(i - 1);
					t.setMaltdepid(i);
					t.setMaltdephead(headIndex);
					if (headIndex != 0) {
						String label = maltNode.getHeadEdge().getLabelSymbol(table);
						t.setMaltdeprel(label);
					} else {
						t.setMaltdeprel("ROOT");
					}
				}
			} catch (MaltChainedException e) {
				throw new AnalysisEngineProcessException(e);
			}		
		}
		log.debug("Finished malt parser annotation");
	}
}
