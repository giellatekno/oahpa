package werti.uima.ae;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;
import java.util.TreeMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.log4j.Logger;
import org.apache.uima.UimaContext;
import org.apache.uima.analysis_component.JCasAnnotator_ImplBase;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.cas.text.AnnotationIndex;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceInitializationException;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.parser.Tag;
import org.jsoup.select.Elements;

import weka.classifiers.Classifier;
import weka.core.Attribute;
import weka.core.FastVector;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.SerializationHelper;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Remove;

import werti.uima.types.annot.PlainTextSentenceAnnotation;
import werti.uima.types.annot.RelevantText;
import werti.uima.types.annot.Token;

/**
 * HTML content type annotator:
 * 
 * Classifies relevant text spans into headline, body, boilerplate, etc.
 *
 * @author Adriane Boyd
 */
public class HTMLContentTypeAnnotator extends JCasAnnotator_ImplBase {

	public static String className = "wertiview";
	
	private static Element emptyElement;
	
	// margin for double comparison
	public static final double EPSILON = Math.pow(10, -14);
	
	// whether to perform smoothing
	private static final boolean DO_SMOOTHING = true;
	

	// CACHES
	
	// assigns a unique id to each element
	private static HashMap<Element,Integer> id = new HashMap<Element,Integer>();
	private static int curId = 0;
	// list of ids of all WERTi spans (will be initialized as soon as we know 
	// how many WERTi spans we have)
	private static int[] wertiIds = null;
	private static int wertiIdsIdx = 0;
	
	// feature cache; access: features[featureName][wertiId]
	private static HashMap<String,Double[]> features = new 
		HashMap<String,Double[]>();
	
	// the token annotation for this document
	private static AnnotationIndex tokenIndex = null;
	private static AnnotationIndex sentIndex = null;
	
	// caches for tokenized and sent-detected text (keys are ids)
	private static ArrayList<String[]> tokenCache = new ArrayList<String[]>();
	private static ArrayList<String[]> sentenceCache = new 
		ArrayList<String[]>();
	
	// cache for the div/td word counts; the empty element is the key for the 
	// sum of all words outside any div/td
	private static HashMap<Element,Double> divTdWordCounts = new 
		HashMap<Element,Double>();

	// number of words in the document that are not in an <a> tag
	private static int docNonAnchorWordCount = 0;
	// the same for every block
	private static ArrayList<Integer> nonAnchorWordCount = new ArrayList<Integer>();
	

	
	// LISTS
	
	// list of all feature names
	private static final String[] featureNames = {"p","p immediate","a",
		"a immediate","h1-6","list","split p","split br","split inline",
		"split block","char alpha","char digit","char punct","char white",
		"char alphaRel","char digitRel","char punctRel","char whiteRel",
		"char otherRel","token alpha","token digit","token other",
		"token alphaRel","token digitRel","token otherRel",
		"token avgTokenLength","token numUpperTokens",
		"token ratioUpperTokens","token numAllUpperTokens",
		"token ratioAllUpperTokens","sent numSentences","sent avgNumWords",
		"sent sentBoundRel","is sentence end","pattern bullet 0 contained",
		"pattern bullet 1 contained","div/td word ratio","id","idRel",
		"text density","link density","num words this",
		"sharesPWithPrePrev","sharesDivWithPrePrev","sharesTdWithPrePrev",
		"sharesPWithPrev","sharesDivWithPrev","sharesTdWithPrev",
		"sharesPWithNext","sharesDivWithNext","sharesTdWithNext",
		"sharesPWithPostNext","sharesDivWithPostNext","sharesTdWithPostNext"};
	// The following attribute indices are all zero-based.
	// attribute index of 'sent numSentences'
	private static final int numSentAttrIdx = 30;
	// attribute index of the 'id' attribute
	private static final int idAttrIdx = 37;
	// index of "num words this" in this list
	private static final int numWordsThisAttrIdx = 42;
	// number of 'shares*' features
	private static final int numSharesFeats = 12;
	// index in the feature name list where the 'shares*' features start
	private static final int sharesFeatsStartIdx = featureNames.length-numSharesFeats;
	// attribute indices of the 'shares*' attributes
	private static final int sharesAttrsStart = 42;
	// (end is exclusive)
	private static final int sharesAttrsEnd = sharesAttrsStart+numSharesFeats;
	// attribute index of the 'Classification' attribute (filled by the first classifier)
	private static final int classAttrIdx = 61;
	// attribute index of the 'annotation' attribute (filled by the 2nd classifier)
	private static final int annotationAttrIdx = 64;
	
	// names of the features that involve more than one span
	private static final String[] additionalFeatureNames = {"p/c num words",
		"p/c text density","|p-c| text density","num words prev",
		"num words next"};
	private static final int numWordsPrevAttrIdx = featureNames.length + 3;
	private static final int numWordsNextAttrIdx = featureNames.length + 4;
	
	// name of the class attribute
	private static final String classFeatureName = "annotation";
	
	// possible values for the class attribute
	private static final String[] classFeatureValues = {
		"Not content_Related content", "Headline", "Supplemental", 
		"Full text_Comments"};
	
	// the CSS classes must not contain spaces or special chars
	private static final String boilerplate = "boilerplate";
	private static final String headline = "headline";
	private static final String supplemental = "supplemental";
	private static final String content = "content";
	private static final String[] cssClasses = {boilerplate, headline, 
		supplemental, content};
	private static TreeMap<String,String> classToCss = null;
	
	// useful lists of tags that can be seen as one 'class' of tags
	private static final String[] TAGCLASS_LIST = {"li", "ul", "ol"};
	private static final String[] TAGCLASS_IGNORE = {"script", "noscript", 
		"form", "object", "embed", "head", "meta", "link", "title", "applet", 
		"style"};
	
	
	
	// PATTERNS
	
	// pattern that matches anything
	private static final Pattern PAT_ANYTHING = Pattern.compile(".*");
	
	// tag name patterns
	private static final Pattern PAT_TAGNAME_DIV = Pattern.compile("[Dd][Ii][Vv]");
	private static final Pattern PAT_TAGNAME_TD = Pattern.compile("[Tt][Dd]");
	private static final Pattern PAT_TAGNAME_P = Pattern.compile("[Pp]");

	// from boilerpipe, for tokenizer
	private static final Pattern PAT_WORD_BOUNDARY = Pattern.compile("\\b");
	private static final Pattern PAT_NOT_WORD_BOUNDARY = Pattern
		.compile("[\u2063]*([\\\"'\\.,\\!\\@\\-\\:\\;\\$\\?\\(\\)/])[\u2063]*");
	
	// matches any tag name except for <a>
	private static final Pattern PAT_NON_ANCHOR_TAG = Pattern
		.compile(".*[^a]+.*");

	// was needed for feature extraction of training data
	//private static final String PAT_ANNOTATION = "x-nc-sel[0-5]";
	
	// a token that ends a sentence (matches "." and "word.")
	private static final Pattern PAT_SENTENCE_END_STRICT = Pattern
		.compile("[.?!]+");
	private static final Pattern PAT_NON_SENTENCE_END = Pattern
		.compile(".*[^.?!]+");

	// character class regexps
	private static final Pattern PAT_UPPER = Pattern.compile("\\p{Lu}");
	private static final Pattern PAT_ALL_UPPER = Pattern.compile("\\p{Lu}+");
	private static final Pattern PAT_ALPHAS = Pattern.compile("(\\p{L})+");
	private static final Pattern PAT_DIGITS = Pattern.compile("(\\p{N})+");
	private static final Pattern PAT_ALPHADIGITS = Pattern
		.compile("[\\p{L}\\p{N}]+");
	private static final Pattern PAT_NON_ALPHAS = Pattern.compile("[^\\p{L}]+");
	private static final Pattern PAT_NON_DIGITS = Pattern.compile("[^\\p{N}]+");
	private static final Pattern PAT_NON_PUNCTS = Pattern.compile("[^\\p{P}]+");
	private static final Pattern PAT_NON_WHITES = Pattern.compile("[^\\p{Z}]+");

	// regexps for the bullet feature
	private static final Pattern[] PAT_BULLET = {
		Pattern.compile("\\p{Pd}.*"), 
		Pattern.compile("[\\p{N}\\p{L}]\\..*")};
	
	
	
	// for smoothing

	// J48 cannot handle missing values, so use a replacement instead
	private static final String MISSING_REPLACEMENT = "missing";
	
	// size of the block n-gram to consider
	private static final int ngramSize = 5;
	// index at which the n-gram should start (relative to the current block)
	private static final int ngramStartIdx = - (int) (ngramSize/2);
	
	// what to call the n-gram features: name prefixes
	private static final String[] ngramPrefixes = {"prePre", "pre", "", "post", "postPost"};
	

	
	private static final Logger log =
		Logger.getLogger(HTMLContentTypeAnnotator.class);
	// the first classifier
	private static Classifier cls;
	// the second classifier (for smoothing)
	private static Classifier smoother;
	
	@Override
	public void initialize(UimaContext aContext)
			throws ResourceInitializationException {
		super.initialize(aContext);
		
		// load weka model (use hard-coded path in /usr/local/werti from 
		// desc/annotator/HtmlContentTypeAnnotator.xml, can switch to 
		// WERTiContext later)
		// some API examples are here: https://svn.scms.waikato.ac.nz/svn/weka/branches/stable-3-6/wekaexamples/src/main/java/wekaexamples/classifiers/WekaDemo.java
		log.debug("Loading model");
		String modelFileName =  (String)aContext.getConfigParameterValue("htmlContentModelLocation");
		try {
			cls = (Classifier) SerializationHelper.read(modelFileName);
		}
		catch (Exception e) {
			log.debug("could not load model " + modelFileName);
			return;
		}
				
		String smoothingModelFileName =  (String)aContext.getConfigParameterValue("htmlContentSmootherModelLocation");
		try {
			smoother = (Classifier) SerializationHelper.read(smoothingModelFileName);
		}
		catch (Exception e) {
			log.debug("could not load smoother model " + smoothingModelFileName);
			StackTraceElement[] stackTrace = e.getStackTrace();
			for (StackTraceElement element : stackTrace){
				log.debug(element.toString());
			}
			return;
		}

		/*try {
			
		} catch (WERTiContextException wce) {
			throw new ResourceInitializationException(wce);
		}*/
	}

	/**
	 * Classifies relevant text spans into headline, body, boilerplate, etc.
	 * 
	 * @param cas The document's cas.
	 */
	@SuppressWarnings("unchecked")
	public void process(JCas cas) throws AnalysisEngineProcessException {
		
		classToCss = new TreeMap<String,String>();
		// map the internal class names to the CSS class names
		for (int i=0; i<classFeatureValues.length; i++){
			classToCss.put(classFeatureValues[i], cssClasses[i]);
		}

		log.debug("Starting HTML content type annotation");
		
		// reset all document-dependent variables
		id = new HashMap<Element,Integer>();
		curId = 0;
		wertiIdsIdx = 0;
		features = new HashMap<String,Double[]>();
		divTdWordCounts = new HashMap<Element,Double>();
		docNonAnchorWordCount = 0;
		nonAnchorWordCount = new ArrayList<Integer>();
		
		// get HTML from CAS
		String htmlString = cas.getDocumentText();
		// parse with Jsoup
		Document doc = Jsoup.parse(htmlString);
		// find all wertiview spans
		Elements wertiTextSpans = doc.getElementsByClass(className);
		
		// prepare to iterate over relevant text pieces
		final AnnotationIndex rtIndex = cas.getAnnotationIndex(RelevantText.type);
		tokenIndex = cas.getAnnotationIndex(Token.type);
		sentIndex = cas.getAnnotationIndex(PlainTextSentenceAnnotation.type);
		//log.debug("sentence beginnings:");
		Iterator<PlainTextSentenceAnnotation> sentIt = sentIndex.iterator();
		/*while (sentIt.hasNext()){
			log.debug(sentIt.next().getBegin());
		}*/
		// iterator over relevant text pieces for feature extraction
		final Iterator<RelevantText> rtIt = rtIndex.iterator();
		// iterator for document counts
		final Iterator<RelevantText> rtIt1 = rtIndex.iterator();
		// iterator for classification
		final Iterator<RelevantText> rtIt2 = rtIndex.iterator();

		// count number of words outside <a> tags and set IDs
		docCounts(doc.body(), false, wertiTextSpans, rtIt1);
		
		// initialize wertiIds
		int numWertiSpans = wertiTextSpans.size();
		wertiIds = new int[numWertiSpans];
		
		// create an empty span to use as padding for the beginning/end
		// surrounding context
		emptyElement = new Element(Tag.valueOf("span"), doc.baseUri());
		
		/* GENERAL IDEA:
		 * - iterate over all WERTi spans (with context) and compute all 
		 *   features, cache the feature values; add each span's id to a list 
		 *   of ids of WERTi spans
		 * - iterate over this id list and print the features; probably have 
		 *   different print methods for Kohlschütter's features and 'our' 
		 *   features
		 */
		
		// prepare the feature cache
		for (int i=0; i<featureNames.length; i++){
			features.put(featureNames[i], new Double[numWertiSpans]);
		}
		features.put("div/td word count", new Double[numWertiSpans]);

/*		// iterate over the spans with one span before/after as context
		Iterator<Element> spanIt = wertiTextSpans.listIterator();

		Element prevElement = emptyElement;
		Element currentElement = spanIt.hasNext() ? spanIt.next() : emptyElement;
		Element nextElement = spanIt.hasNext() ? spanIt.next() : emptyElement;
		
		// iterate over RelevantText spans and extract features; store them in 
		// caches
		while (rtIt.hasNext()) {
			RelevantText rt = rtIt.next();
			
			// extract the features for this span
			if (currentElement != emptyElement)
				extractFeatures(prevElement, currentElement, rt);
			else
				log.debug("encountered empty element in JSoup parse");

			// find the next wertiview span in the JSoup parse
			if (spanIt.hasNext()) {
				prevElement = currentElement;
				currentElement = nextElement;
				nextElement = spanIt.next();
			}
			else{
				prevElement = currentElement;
				currentElement = nextElement;
				nextElement = emptyElement;
			}
		}
*/

		// extract features and cache the values
		for (int index=0; index<wertiTextSpans.size(); index++){
			RelevantText rt = rtIt.next();
			// find current element and 4 elements around it
			Element prePrevElement = emptyElement;
			if (0 <= index-2){
				prePrevElement = wertiTextSpans.get(index-2);
			}
			Element prevElement = emptyElement;
			if (0 <= index-1){
				prevElement = wertiTextSpans.get(index-1);
			}
			Element currentElement = wertiTextSpans.get(index);
			Element nextElement = emptyElement;
			if (index+1 < wertiTextSpans.size()){
				nextElement = wertiTextSpans.get(index+1);
			}
			Element postNextElement = emptyElement;
			if (index+2 < wertiTextSpans.size()){
				postNextElement = wertiTextSpans.get(index+2);
			}
			
			// extract features for the current element
			extractFeatures(prePrevElement, prevElement, currentElement, 
					nextElement, postNextElement, rt);
		}

		// compute the div/td word ratios from the div/td word counts
		for (int myWertiId=0; myWertiId<wertiIds.length; myWertiId++){
			double myDivTdWordCount = features.get("div/td word count")[myWertiId];
			double myDivTdWordRatio = myDivTdWordCount / docNonAnchorWordCount;
			features.get("div/td word ratio")[myWertiId] = myDivTdWordRatio;
		}
		
		Instances dataset = prepareDataset();
		// set the class attribute
		dataset.setClassIndex(classAttrIdx);
		
		// create Weka Instances from the cached features
		dataset = feat2instances(dataset);

		// classification cache (necessary for lookahead in smoothing)
		List<String> classificationCache = new ArrayList<String>(dataset.numInstances());
		
		// filter to apply before the first classifier
		Instances firstDataset = getFirstDataset(dataset);
		
		// classify the instances using the first classifier and add the values 
		// for the 'shares*' features
		for (int i=0; i<firstDataset.numInstances(); i++){
			Instance inst = firstDataset.instance(i);
			// default class is 'boilerplate'
			String classification = classFeatureValues[0];
			try{
				int classificationIdx = (int) cls.classifyInstance(inst);
				classification = classFeatureValues[classificationIdx];
				log.debug("classified as: " + classification);
			}
			catch (Exception exception){
				// instances that cause trouble are regarded as boilerplate
				log.debug("could not be classified; exception: " + exception);
			}
			// cache the classification
			classificationCache.add(classification);
		}

		// add values for classification lookaround
		dataset = addLookaroundAttr(dataset, classificationCache);
		// filter for smoothing
		Instances secondDataset = getSecondDataset(dataset);
		
		// smooth the classification: apply a second classifier
		log.debug("smoothing classification...");
		for (int i=0; i<secondDataset.numInstances(); i++){
			RelevantText rt = rtIt2.next();
			Instance inst = secondDataset.instance(i);
			
			// default class is the one chosen by the first classifier
			String classification = classToCss.get(classificationCache.get(i));
			if (DO_SMOOTHING){
				try {
					int classificationIdx = (int) smoother.classifyInstance(inst);
					classification = cssClasses[classificationIdx];
					//log.debug("classified as: " + classification);
				} 
				catch (Exception exception) {
					// instances that cause trouble are ignored
					log.debug("could not be classified; exception: " + exception);
				}
			}
			
			// set this block's content type
			rt.setHtmlContentType(classification);
		}
		log.debug("done smoothing.");
		
		log.debug("Finished HTML content type annotation");
	}

	/**
	 * extract simple HTML features for a relevant element e.
	 * @param prev the preceding relevant element
	 * @param e the element itself
	 * @param rt this element's corresponding RelevantText annot. object
	 */
	private static void extractFeatures(Element prePrev, Element prev, Element e, Element next, Element postNext, RelevantText rt) {
		final Elements parents = e.parents();
		final Element immediateParent = getImmediateParent(parents);
		final String text = rt.getCoveredText().trim();

		// find the tokens and sentences in this span, using the
		// information from the existing tokenization
		List<Token> tokenList = tokenize(rt);
		List<PlainTextSentenceAnnotation> sentList = sentDetect(rt);
		
		//log.debug("Text starting at index: " + rt.getBegin());
		//log.debug("Text ending at index: " + rt.getEnd());
		//log.debug("TEXT::" + rt.getCoveredText() + "::TEXT");
		//log.debug("Number of tokens: " + tokenList.size());
		//log.debug("Number of sentences: " + sentList.size());
		
		int myId = id.get(e);
		wertiIds[wertiIdsIdx] = myId;

		// for debugging:
		/*System.out.print("\n" + e.html() + "¶");
		System.out.println("<" + immediateParent.tagName() + ">");*/

		// container features
		features.get("p")[wertiIdsIdx] = (double) toInt(isIn(parents, "p"));
		features.get("p immediate")[wertiIdsIdx] = (double) toInt(
				isImmediateParent(immediateParent, "p"));
		features.get("a")[wertiIdsIdx] = (double) toInt(isIn(parents, "a"));
		features.get("a immediate")[wertiIdsIdx] = (double) toInt(
				isImmediateParent(immediateParent, "a"));
		features.get("h1-6")[wertiIdsIdx] = (double) toInt(
				isInHeadline(parents));
		features.get("list")[wertiIdsIdx] = (double) toInt(
				isInClass(parents, TAGCLASS_LIST));
		
		// split features
		final Elements splitElements = getElementsSincePrev(prev, e);
		features.get("split p")[wertiIdsIdx] = (double) countSplits(splitElements, "p");
		features.get("split br")[wertiIdsIdx] = (double) countSplits(splitElements, "br");
		final int numBlock = countSplitsBlock(splitElements);
		features.get("split inline")[wertiIdsIdx] = (double) (splitElements.size()-numBlock);
		features.get("split block")[wertiIdsIdx] = (double) numBlock;
		
		// the letters from the current text
		String[] letters = new String[1];
		
		// char features
		double[] charCounts = charCounts(e.ownText(), letters);
		String[] charFeatNames = {"char alpha","char digit","char punct",
				"char white","char alphaRel","char digitRel","char punctRel",
				"char whiteRel","char otherRel"};
		for (int i=0; i<charCounts.length; i++)
			features.get(charFeatNames[i])[wertiIdsIdx] = charCounts[i];
				
		// token features
		double[] tokenCounts = tokenAndSentenceCounts(text, tokenList, sentList);
		String[] tokenFeatNames = {"token alpha","token digit","token other",
				"token alphaRel","token digitRel","token otherRel",
				"token avgTokenLength","token numUpperTokens",
				"token ratioUpperTokens","token numAllUpperTokens",
				"token ratioAllUpperTokens","sent numSentences",
				"sent avgNumWords","sent sentBoundRel"};
		for (int i=0; i<tokenCounts.length; i++)
			features.get(tokenFeatNames[i])[wertiIdsIdx] = tokenCounts[i];
		
		// sentence end
		features.get("is sentence end")[wertiIdsIdx] = (double) toInt(
				isSentenceEnd(text));
		
		// bullet
		boolean[][] bulletMnC = matchedAndContained(text, PAT_BULLET);
		for (int i=0; i<=1; i++){
			features.get("pattern bullet " + i + " contained")[wertiIdsIdx] = (double) toInt(bulletMnC[1][i]);
		}
		
		// div and td groups
		features.get("div/td word count")[wertiIdsIdx] = divTdWordCount(e.parents());
		
		// position (absolute and relative)
		features.get("id")[wertiIdsIdx] = (double) myId;
		features.get("idRel")[wertiIdsIdx] = (double) myId / curId;
		
		// text density
		features.get("text density")[wertiIdsIdx] = textDensity(tokenList);
		
		//System.out.print("|"); // for debugging
		// link density
		features.get("link density")[wertiIdsIdx] = linkDensity(parents, rt);
		
		features.get("num words this")[wertiIdsIdx] = (double) 
			tokenize(rt).size();
		
		// does this block share a <p>, <div>, or <td> parent with one of its 
		// neighbor blocks? (used only for smoothing)
		boolean[] sharesArray = sharesParentWithNeighbor(prePrev, prev, e, next, postNext);
		for (int i=0; i<numSharesFeats; i++){
			features.get(featureNames[sharesFeatsStartIdx+i])[wertiIdsIdx] 
				= (double) toInt(sharesArray[i]);
		}

		wertiIdsIdx += 1;
	}
	
	/**
	 * prepare the Weka dataset that is used for both classifiers.
	 */
	private static Instances prepareDataset(){
		// list of all attributes
		FastVector attrList = new FastVector(featureNames.length + additionalFeatureNames.length + 1);

		// add normal features
		for (String attrName : featureNames){
			attrList.addElement(new Attribute(attrName));
		}

		// add features affecting more than one span
		for (String attrName : additionalFeatureNames){
			attrList.addElement(new Attribute(attrName));
		}

		// possible values for the class attributes: the 4 HTML content types
		FastVector attrTypeClassification = new FastVector();
		for (String contentType : classFeatureValues){
			attrTypeClassification.addElement(contentType);
		}
		FastVector attrTypeClassificationNoMissing = (FastVector) attrTypeClassification.copy();
		// replacement value for missing values
		attrTypeClassification.addElement(MISSING_REPLACEMENT);
		for (int i=0; i<ngramSize; i++){
			FastVector type = attrTypeClassification;
			// the value of this block's classification will not be missing
			if (i == -ngramStartIdx){
				type = attrTypeClassificationNoMissing;
			}
			Attribute attr = new Attribute(ngramPrefixes[i] + "Classification", type);
			attrList.addElement(attr);
		}
		
		// attribute for final classification (after both classifiers have been applied)
		Attribute attr = new Attribute(classFeatureName, attrTypeClassificationNoMissing);
		attrList.addElement(attr);

		// create the dataset object from the list of attributes
		Instances dataset = new Instances("wertiview_dataset", attrList, wertiIdsIdx);
		return dataset;
	}
	
	/**
	 * returns Integer.MIN_VALUE if the given value is -1, +/-Infinity, or NaN, 
	 * otherwise returns the given value itself.
	 */
	private static double getExceptMinusOne(Double value){
		// -1 is treated as missing value
		if (Math.abs(value - (-1)) < EPSILON
			|| value.equals(Double.NaN) 
			|| value.equals(Double.POSITIVE_INFINITY) 
			|| value.equals(Double.NEGATIVE_INFINITY)){

			return Integer.MIN_VALUE;
		}
		else{
			return value;
		}
	}

	/**
	 * @param dataset the dataset that the data belongs to
	 * @return a dataset to be fed to a Weka classifier (the parameter filled with instances)
	 */
	private static Instances feat2instances(Instances dataset){
		// loop over all wertiview spans
		for (int myWertiId=0; myWertiId<wertiIds.length; myWertiId++){
			// create Instance
			Instance inst = new Instance(dataset.numAttributes());
			// add it to the dataset
			inst.setDataset(dataset);
			
			// set its weight (proportional to token count)
			String numWordsThisFeatName = featureNames[numWordsThisAttrIdx];
			double numWordsThis = getExceptMinusOne(features.get(numWordsThisFeatName)[myWertiId]);
			inst.setWeight(numWordsThis);
			
			// loop over all features
			for (int i=0; i<featureNames.length; i++){
				String fn = featureNames[i];
				double value = getExceptMinusOne(features.get(fn)[myWertiId]);
				inst.setValue(i, value);
			}
			
			int plus = 0;

			// qutotients and deltas
			if (myWertiId == 0){
				for (; plus<3; plus++){
					double value = getExceptMinusOne(-1.0);
					inst.setValue(featureNames.length+plus, value);
				}
			}
			else{
				// p/c num words
				Double[] numWordsArray = features.get("num words this");
				double value = getExceptMinusOne(numWordsArray[myWertiId-1] / numWordsArray[myWertiId]);
				inst.setValue(featureNames.length+plus, value);
				plus++;
				
				// p/c text density
				Double[] textDensityArray = features.get("text density");
				value = getExceptMinusOne(textDensityArray[myWertiId-1] / textDensityArray[myWertiId]);
				inst.setValue(featureNames.length+plus, value);
				plus++;
				
				// |p-c| text density
				value = getExceptMinusOne(Math.abs(textDensityArray[myWertiId-1] - textDensityArray[myWertiId]));
				inst.setValue(featureNames.length+plus, value);
				plus++;
			}

			// num words prev
			if (myWertiId == 0){
				double value = getExceptMinusOne(-1.0);
				inst.setValue(featureNames.length+plus, value);
				plus++;
			}
			else{
				double value = getExceptMinusOne(features.get("num words this")[myWertiId-1]);
				inst.setValue(featureNames.length+plus, value);
				plus++;
			}
			
			// num words next
			if (myWertiId == wertiIds.length-1){
				double value = getExceptMinusOne(-1.0);
				inst.setValue(featureNames.length+plus, value);
				plus++;
			}
			else{
				double value = getExceptMinusOne(features.get("num words this")[myWertiId+1]);
				inst.setValue(featureNames.length+plus, value);
				plus++;
			}
			
			// add the instance to the dataset
			if (dataset.checkInstance(inst)){
				dataset.add(inst);
			}
			else{
				log.debug("the following instance is not compatible with the dataset: " + inst);
			}
		}
		return dataset;
	}
	
	/**
	 * removes attributes not necessary for the first classifier.
	 * @param dataset the dataset to be passed through the filter
	 * @return the filtered dataset
	 */
	private static Instances getFirstDataset(Instances dataset){
		Instances firstDataset = null;
		Remove filter = new Remove();
		int j = 0;
		int[] attributeIndices = new int[(sharesAttrsEnd-sharesAttrsStart) + (ngramSize-1) + 1];
		// remove the 'shares*' attributes
		for (int i=sharesAttrsStart; i<sharesAttrsEnd; i++){
			attributeIndices[j] = i;
			j++;
		}
		// remove the classification lookaround attributes
		for (int i=classAttrIdx+ngramStartIdx; i<classAttrIdx+ngramStartIdx+ngramSize ; i++){
			if (i != classAttrIdx){
				attributeIndices[j] = i;
				j++;
			}
		}
		// remove the 'annotation' attribute
		attributeIndices[j++] = annotationAttrIdx;
		filter.setAttributeIndicesArray(attributeIndices);
		try {
			filter.setInputFormat(dataset);
			firstDataset = Filter.useFilter(dataset, filter);
		}
		catch (Exception e) {
			StackTraceElement[] stackTrace = e.getStackTrace();
			for (StackTraceElement element : stackTrace){
				log.debug(element.toString());
			}
		}
		// (apparently no need to rename 'Classification' to 'annotation')
		return firstDataset;
	}
	
	/**
	 * removes attributes not necessary for the smoother.
	 * @param dataset the dataset to be passed through the filter
	 * @return the filtered dataset
	 */
	private static Instances getSecondDataset(Instances dataset){
		Instances secondDataset = null;
		Remove filter = new Remove();
		int j = 0;
		int[] attributeIndices = new int[(featureNames.length-numSharesFeats-1) + additionalFeatureNames.length];
		// remove all regular attributes except for 'sent numSentences', 
		// 'num words this' and the 'shares*' attributes
		for (int i=0; i<featureNames.length-numSharesFeats-1; i++){
			if (i != numSentAttrIdx){
				attributeIndices[j] = i;
				j++;
			}
		}
		// remove the quotients and deltas (except for 'num words prev' and 
		// 'num words next')
		for (int i=featureNames.length; i<featureNames.length+additionalFeatureNames.length ; i++){
			if (i != numWordsPrevAttrIdx && i != numWordsNextAttrIdx){
				attributeIndices[j] = i;
				j++;
			}
		}
		filter.setAttributeIndicesArray(attributeIndices);
		try {
			filter.setInputFormat(dataset);
			secondDataset = Filter.useFilter(dataset, filter);
		}
		catch (Exception e) {
			log.debug(e.getStackTrace());
		}
		// set the class attribute
		secondDataset.setClassIndex(secondDataset.numAttributes()-1);
		return secondDataset;
	}
	
	/**
	 * add the classification and other properties of the surrounding blocks 
	 * as features. (Set the feature values.)
	 */
	private static Instances addLookaroundAttr(Instances dataset, List<String> classCache){
		// iterate over all instances
		for (int i=0; i<dataset.numInstances(); i++){
			Instance inst = dataset.instance(i);
			
			// where the new attributes start
			int newAttrIdx = dataset.numAttributes() - 1 - ngramSize;
			
			// lookaround in the classification cache
			for (int j=i+ngramStartIdx; j<i+(ngramSize+ngramStartIdx); j++){
				if (0 <= j && j < classCache.size()){
					String classification = classCache.get(j);
					inst.setValue(newAttrIdx, classification);
				}
				// if the neighboring block doesn't exist
				else{
					inst.setValue(newAttrIdx, MISSING_REPLACEMENT);
				}
				newAttrIdx++;
			}
		}
		
		return dataset;
	}

	
//----------------------------------------------------------------------------
	
	/**
	 * fills the id map and sets docNonAnchorWordCount, the number of tokens 
	 * outside <a> tags.
	 * Preorder traversal is used.
	 * @param isInA true iff e is an <a> tag itself or contained in one
	 * @param wertiTextSpans all elements marked as wertiview spans
	 * @param rtIt1 an iterator over the RelevantText chunks, for tokenization
	 */
	private static void docCounts(Element e, boolean isInA, Elements wertiTextSpans, Iterator<RelevantText> rtIt1){
		// special treatment for <a> tags
		if (e.tagName().equals("a")){
			isInA = true;
		}
		
		// assign an id
		id.put(e, curId);
		curId++;
		
		int numTokens = 0;
		// outside of any <a> tag
		if ( ! isInA){
			// do we have OpenNLP tokenization data for this element? i.e. is this 
			// a relevant text piece?
			if (wertiTextSpans.contains(e) && rtIt1.hasNext()){
				// get those tokens
				RelevantText rt = rtIt1.next();
				List<Token> tokenList = tokenize(rt);
				numTokens = tokenList.size();
			}
			else{
				// tokenize 'by hand'
				String[] tokens = tokenize(e);
				numTokens = tokens.length;
			}
			docNonAnchorWordCount += numTokens;
		}
		// cache the non-anchor word count
		nonAnchorWordCount.add(numTokens);
		
		// RECURSION (automatic BASE CASE: e has no children)
		for (Element child : e.children()){
			docCounts(child, isInA, wertiTextSpans, rtIt1);
		}
	}
	
	/**
	 * returns true iff e is not a WERTi or annotation span and is thus very 
	 * likely to have appeared in the original HTML document.
	 */
	private static boolean wasInOriginalHtml(Element e){
		// we can only recognize our inserted spans by their class names
		Set<String> classes = e.classNames();
		// if it is a werti span, return false
		return ! classes.contains(className);
		
		// was needed for feature extraction on training data
		/*if (classes.contains(className)){
			return false;
		}
		// if the tag doesn't belong to the werti class
		else{
			// does the tag belong to any annotation class?
			boolean contains = false;
			for (String c : classes)
				contains = contains || c.matches(PAT_ANNOTATION);
			return ! contains;
		}*/
	}
	
	/**
	 * returns true iff one of the parents is a tagName tag
	 */
	private static boolean isIn(Elements parents, String tagName) {
		for (Element p : parents) {
			if (p.tagName().toLowerCase().equals(tagName)) {
				return true;
			}
		}

		return false;
	}
	
	/**
	 * returns true iff one of the parents is a h1...h6 tag (uses regex)
	 */
	private static boolean isInHeadline(Elements parents){
		for (Element p : parents) {
			if (p.tagName().toLowerCase().matches("h[1-6]")) {
				return true;
			}
		}

		return false;
	}
	
	/**
	 * returns true iff one of the parents is a tag listed in tagList (see 
	 * constants above for useful tag lists)
	 */
	private static boolean isInClass(Elements parents, String[] tagList){
		for (Element p : parents) {
			for (String tagName : tagList){
				if (p.tagName().toLowerCase().equals(tagName)) {
					return true;
				}
			}
		}

		return false;
	}
	
	/**
	 * returns the node that was the immediate parent of e in the original 
	 * HTML code. Skips all werti and annotation spans.
	 */
	private static Element getImmediateParent(Elements parents){
		return getImmediateParent(parents, PAT_ANYTHING);
	}
	
	/**
	 * returns the closest parent that matches the regex reTagName. Skips all 
	 * werti and annotation spans.
	 */
	private static Element getImmediateParent(Elements parents, Pattern tagPattern){
		for (Element p : parents){
			if (wasInOriginalHtml(p) 
					&& tagPattern.matcher(p.tagName()).matches())
				return p;
		}
		// if we couldn't find any non-werti non-annotation parent, return the 
		// innermost parent
		return parents.get(0);
	}

	/**
	 * returns true iff parent is a tagName tag
	 */
	private static boolean isImmediateParent(Element parent, String tagName) {
		return parent.tagName().toLowerCase().equals(tagName);
	}

	/**
	 * return true iff this tag should be ignored.
	 */
	private static boolean isIgnored(String tagName){
		for (String toIgnore : TAGCLASS_IGNORE){
			if (tagName.equals(toIgnore)) 
				return true;
		}
		return false;
	}
	
	/**
	 * return all intermediate and leaf nodes encountered on the way from prev 
	 * to e (or an empty list if prev is an emptyElement).
	 */
	private static Elements getElementsSincePrev(Element prev, Element e){
		// if prev is empty, return an empty list
		if (prev.equals(emptyElement)){
			return new Elements();
		}
		else{
			/* - traverse the whole tree from prev to e
			 * - return a list of all nodes encountered on the way
			 */
			// start at prev
			Element curNode = prev;
			// rval
			Elements inBetween = new Elements();
			
			boolean doIgnore = false;
			// as soon as we reach e, we are finished
			while ( ! curNode.equals(e)){
				doIgnore = false;
				// if this is an IGNORE node, ignore it
				if (isIgnored(curNode.tagName())){
					doIgnore = true;
				}
				else{
					// if it is a werti or annotation span, don't add it
					if (wasInOriginalHtml(curNode)){
						// add the node
						inBetween.add(curNode);
					}
				}
				
				// is there a level below the current?
				if ( ! doIgnore && curNode.children().size() != 0){
					// go deeper
					curNode = curNode.children().first();
				}
				
				// if there is no deeper level:
				else{
					// is there a next sibling?
					if (curNode.nextElementSibling() != null){
						// go to the next sibling
						curNode = curNode.nextElementSibling();
					}
					
					// if there is no next sibling
					else{
						// go up until there is a next sibling
						while (curNode.nextElementSibling() == null){
							curNode = curNode.parent();
							// also add the closing tags of these nodes while 
							// we're going up
							if ( ! isIgnored(curNode.tagName()) 
									&& wasInOriginalHtml(curNode)){
								inBetween.add(curNode);
							}
						}
						// go to that next sibling
						curNode = curNode.nextElementSibling();
					}
				}
			}
			// return the list
			return inBetween;
		}
	}
	
	/**
	 * returns the number of html tags with tagName in splitElements.
	 */
	private static int countSplits(Elements splitElements, String tagName){
		tagName = tagName.toLowerCase();
		int count = 0;
		for (Element splitE : splitElements){
			if (splitE.tagName().toLowerCase().equals(tagName)){
				count += 1;
			}
		}
		return count;
	}

	/**
	 * returns the number of block tags in splitElements.
	 */
	private static int countSplitsBlock(Elements splitElements){
		int count = 0;
		for (Element splitE : splitElements){
			if (splitE.isBlock()){
				count += 1;
			}
		}
		return count;
	}
	
	/**
	 * returns, in this order, the absolute and relative counts of letters, 
	 * digits, punctuation chars, whitespace chars, other chars, and vertical 
	 * bars.
	 * Also stores an only-letters version of the text in letters.
	 */
	private static double[] charCounts(String text, String[] letters){
		// total num of chars
		final int len = text.length();
		
		// throw out all non-letters and store the result in letters
		String onlyLetters = PAT_NON_ALPHAS.matcher(text).replaceAll("");
		letters[0] = onlyLetters;

		// delete all unwanted chars and get the length of the rest
		int alpha = onlyLetters.length();
		int digit = PAT_NON_DIGITS.matcher(text).replaceAll("").length();
		int punct = PAT_NON_PUNCTS.matcher(text).replaceAll("").length();
		int white = PAT_NON_WHITES.matcher(text).replaceAll("").length();
		int other = text.length() - alpha - digit - punct - white;
		
		// compute the relative counts from the absolute counts
		double alphaRel = (double) alpha / len;
		double digitRel = (double) digit / len;
		double punctRel = (double) punct / len;
		double whiteRel = (double) white / len;
		double otherRel = (double) other / len;
		
		// put all these values in an array and return it
		double[] rval = {alpha, digit, punct, white, 
				alphaRel, digitRel, punctRel, whiteRel, otherRel};
		return rval;
	}
	
	/**
	 * returns, in this order, the absolute and relative counts of all-letter 
	 * tokens, all-digit tokens, letter-and-digit tokens and other tokens; the 
	 * average length of a token and the number and ratio of tokens starting 
	 * with a uppercase character; the number and ratio of tokens that are 
	 * all-uppercase; the number of sentences, the average 
	 * sentence length (in tokens), and the ratio of sentence boundary markers 
	 * to number of tokens.
	 * This method should work with both a naive whitespace tokenizer and a 
	 * tokenizer that treats punctuation as tokens.
	 */
	private static double[] tokenAndSentenceCounts(String text, List<Token> tokenList, List<PlainTextSentenceAnnotation> sentList){
		final int numTokens = tokenList.size();
		final int numSentences = sentList.size();
		// count the absolute num of tokens in each class
		int alpha = 0, digit = 0, other = 0;
		// sum of all token lengths (to calculate average token length later)
		int sumTokenLengths = 0;
		// number of tokens that start with an uppercase letter
		int numUpperTokens = 0;
		// number of all-uppercase tokens
		int numAllUpperTokens = 0;
		// count words (=tokens that are no sentence boundary marker)
		int numWords = 0;
		
		// traverse all tokens
		for (Token t : tokenList){
			String token = t.getCoveredText();
			// the token consist only of letters
			if (PAT_ALPHAS.matcher(token).matches()){
				alpha += 1;
			}
			// the token consist only of digits
			else if (PAT_DIGITS.matcher(token).matches()){
				digit += 1;
			}
			// the token consist of letters and digits, but no other chars
			else if (PAT_ALPHADIGITS.matcher(token).matches()){
			}
			// the token contains chars other than letters and digits
			else{
				other += 1;
			}
			
			sumTokenLengths += token.length();
			
			// all-uppercase tokens and ones starting with an uppercase char
			if (PAT_ALL_UPPER.matcher(token).matches())
				numAllUpperTokens += 1;
			else if (PAT_UPPER.matcher(token).lookingAt())
				numUpperTokens += 1;

			// words (not tokens!)
			if ( ! PAT_SENTENCE_END_STRICT.matcher(token).matches())
				numWords += 1;
		}
		
		// compute the relative numbers of tokens
		double alphaRel = (double) alpha / numTokens;
		double digitRel = (double) digit / numTokens;
		double otherRel = (double) other / numTokens;
		
		// average token length
		double avgTokenLength = (double) sumTokenLengths / numTokens;
		
		// number and ratio of uppercase tokens
		double ratioUpperTokens = (double) numUpperTokens / numTokens;
		double ratioAllUpperTokens = (double) numAllUpperTokens / numTokens;
		
		// compute the average sentence length in words (not tokens!)
		double avgNumWords = (double) numWords / numSentences;
		
		// ratio of sentence boundary markers to number of tokens
		int sentBound = PAT_NON_SENTENCE_END.matcher(text).replaceAll("")
			.length();
		double sentBoundRel = (double) sentBound / numTokens;
		
		// put together an array of all the values and return it
		double[] rval = {alpha, digit, other, alphaRel, digitRel, 
				otherRel, avgTokenLength, numUpperTokens, 
				ratioUpperTokens, numAllUpperTokens, ratioAllUpperTokens, 
				numSentences, avgNumWords, sentBoundRel};
		return rval;
	}
		
	/**
	 * returns true iff text ends with a sentence end character.
	 */
	private static boolean isSentenceEnd(String text){
		return text.endsWith(".") || text.endsWith("?") || text.endsWith("!");
	}
	
	/**
	 * returns an array of booleans each indicating whether one of the given 
	 * patterns matched and another array of booleans indicating if the 
	 * patterns were contained in text.
	 */
	private static boolean[][] matchedAndContained(String text, Pattern[] patterns){
		boolean[][] rval = new boolean[2][patterns.length];
		for (int i=0; i<patterns.length; i+=1){
			Matcher m = patterns[i].matcher(text);
			rval[0][i] = m.matches();
			rval[1][i] = m.find();
		}
		return rval;
	}

	/**
	 * returns the index of the first regex in patterns found in text or -1 if 
	 * no regex was found. 
	 */
	/*private static int getRegexIdxContained(String text, Pattern[] patterns){
		for (int i=0; i<patterns.length; i+=1){
			if (patterns[i].matcher(text).find())
				return i;
		}
		// if no regex matches, return an illegal value
		return -1;
	}*/

	/**
	 * returns the first div or td tag found in parents. If no such tag is 
	 * found, emptyElement is returned as a dummy tag.
	 */
	private static Element getClosestDivTd(Elements parents){
		for (Element p : parents){
			if (p.tagName().equals("div") || p.tagName().equals("td"))
				return p;
		}
		// if we couldn't find any div or td, return an illegal value
		return emptyElement;
	}
	
	/**
	 * return the number of tokens in e and its children, skipping any <a> tags.
	 */
	private static int numNonAnchorWords(Element e){
		/*// skip <a> tags // unnecessary
		if (e.tagName().equals("a"))
			return 0;*/
		
		// the empty element doesn't have an ID, but it has 0 tokens anyway
		if (e.equals(emptyElement)){
			return 0;
		}
		
		int eId = id.get(e);
		int rval = nonAnchorWordCount.get(eId);
		
		// RECURSION (automatic BASE CASE: e has no children)
		for (Element child : e.children()){
			rval += numNonAnchorWords(child);
		}
		return rval;
	}
	
	/** 
	 * returns the number of tokens in the first <div> or <td> found in 
	 * parents. Excludes tokens that are in <a> tags.
	 */
	private static double divTdWordCount(Elements parents){
		// find the closest enclosing div or td in the parents list
		Element closestDivTd = getClosestDivTd(parents);
		
		// if we have seen this div/td before, get the word count
		if (divTdWordCounts.containsKey(closestDivTd)){
			return divTdWordCounts.get(closestDivTd);
		}
		// if we haven't seen it before
		else{
			// count the words in the div/td
			double newWordCount = numNonAnchorWords(closestDivTd);
			// add it to the storage together with its word count
			divTdWordCounts.put(closestDivTd, newWordCount);
			// return the new word count
			return newWordCount;
		}
	}
	
	/**
	 * text density as described in Kohlschütter.Frankhauser-10
	 */
	private static double textDensity(List<Token> tokenList){

		int numWords = 0;
		int numWrappedLines = 0;
		int currentLineLength = -1; // don't count the first space
		final int maxLineLength = 80;
		int numTokens = 0;
		int numWordsCurrentLine = 0;

		for (Token t : tokenList) {
			numTokens++;
			numWords++;
			numWordsCurrentLine++;
			final int tokenLength = t.getCoveredText().length();
			currentLineLength += tokenLength + 1;
			if (currentLineLength > maxLineLength) { // WRAP
				numWrappedLines++;
				currentLineLength = tokenLength;
				numWordsCurrentLine = 1;
				//System.out.print("\n" + token);
			}
			//else
			//System.out.print(" " + token);
		}
		if (numTokens == 0) {
			return 0;
		}

		int numWordsInWrappedLines;
		if (numWrappedLines == 0) {
			return numWords;
		}
		else {
			numWordsInWrappedLines = numWords - numWordsCurrentLine;
			return (double) numWordsInWrappedLines / numWrappedLines;
		}
	}
	
	/**
	 * does this block share a parent <p>, <div>, or <td> with its neighbor 
	 * blocks?
	 * @return array of booleans, ordered by neighbor block
	 */
	private static boolean[] sharesParentWithNeighbor(Element prePrev, 
		Element prev, Element e, Element next, Element postNext){
		
		// to return
		boolean[] sharesArray = new boolean[numSharesFeats];
		int i = 0;
		
		// which parent tag names to check for
		Pattern[] parentTagNames = {PAT_TAGNAME_P, PAT_TAGNAME_DIV, 
			PAT_TAGNAME_TD};
		
		// this block's parent <p>, <div>, and <td>
		Element[] myParents = new Element[parentTagNames.length];
		for (int j=0; j<parentTagNames.length; j++){
			Pattern patParentTagName = parentTagNames[j];
			myParents[j] = getImmediateParent(e.parents(), patParentTagName);
		}

		// traverse all neighboring blocks
		Element[] neighbors = {prePrev, prev, next, postNext};
		for (Element neighbor : neighbors){
			// traverse all parent tag names
			for (int j=0; j<parentTagNames.length; j++){

				// empty elements cannot share a parent with the current element
				if (neighbor == emptyElement){
					sharesArray[i] = false;
				}
				else{
					// do they have the same parent?
					Pattern patParentTagName = parentTagNames[j];
					Element neighborParent = getImmediateParent(neighbor.parents(), patParentTagName);
					// pointer/object identity ensures it is really the same 
					// element, not just an element with the same tag name
					sharesArray[i] = (myParents[j] == neighborParent);
				}
				i++;
			}
		}
		
		return sharesArray;
	}

	/**
	 * finds the closest parent that is not an <a> tag, then calculates
	 * number of tokens inside <a> tags / number of tokens
	 */
	private static double linkDensity(Elements parents, RelevantText rt){
		// find closest parent that is not an <a> tag
		Element parent = getImmediateParent(parents, PAT_NON_ANCHOR_TAG);
		
		// count the number of tokens inside <a> tags and the total # of tokens
		int numInsideA = 0;
		int numTotal = 0;
		// breadth-first traversal
		LinkedList<Element> q = new LinkedList<Element>();
		q.add(parent);
		while ( ! q.isEmpty()){
			Element cur = q.remove();
			// <a> tags
			if (cur.tagName().equals("a")){
				// add text and text of children to both counts
				int curNum = tokenize(cur.text()).length;
				numInsideA += curNum;
				numTotal += curNum;
			}
			// other tags
			else{
				// add only own text
				numTotal += tokenize(cur).length;
				// enqueue children
				q.addAll(cur.children());
			}
		}
		
		//System.out.print(" parent:<" + parent.tagName() + "> numInsideA:" + numInsideA + " numTotal:" + numTotal + " ");
		// return number of tokens inside <a> tags / number of tokens
		return (numTotal == 0) ? 0 : ((double) numInsideA / numTotal);
	}

	/**
	 * Simple tokenizer copied from boilerpipe:
	 * 
	 * Tokenizes the text and returns an array of tokens.
	 * 
	 * Try to use the other two tokenize methods if possible.
	 * 
	 * @param text
	 *            The text
	 * @return The tokens
	 */
	private static String[] tokenize(final String text) {
		/* The empty string would be tokenized to an array containing the empty 
		 * string. This array would then have length 1, although there are 0 
		 * tokens in the text. This is why we need this special check. */
		if (text.trim().length() == 0){
			String[] emptyArray = new String[0];
			return emptyArray;
		}
		return PAT_NOT_WORD_BOUNDARY
				.matcher(PAT_WORD_BOUNDARY.matcher(text).replaceAll("\u2063"))
				.replaceAll("$1").replaceAll("[ \u2063]+", " ").trim()
				.split("[ ]+");

		//return TOKENIZER.tokenize(text);
	}

	/**
	 * Tokenizes e's OWN text and returns an array of tokens. Works with a 
	 * cache. Does not tokenize anything itself, only calls tokenize(String).
	 * @param e
	 *            The HTML Element
	 * @return The tokens
	 */
	private static String[] tokenize(final Element e) {
		// if e has no id, only tokenize its text
		if (id.get(e) == null)
			return tokenize(e.ownText());
		int eId = id.get(e);
		// look up the value in the cache
		if (eId < tokenCache.size() && tokenCache.get(eId) != null){
			return tokenCache.get(eId);
		}
		else{
			String[] tokens = tokenize(e.ownText());
			// resize the cache /// this takes long, probably better use a HashMap?
			for (int i=tokenCache.size(); i<=eId; i++)
				tokenCache.add(null);
			// add the newly calculated value to the cache
			tokenCache.set(eId, tokens);
			return tokens;
		}
	}
	
	/**
	 * retrieves the tokenization data from OpenNLP
	 */
	@SuppressWarnings("unchecked")
	private static List<Token> tokenize(RelevantText rt){
		// find the number of tokens in this span, using the
		// information from the existing tokenization
		final Iterator<Token> tokenIt = tokenIndex.subiterator(rt);
		List<Token> tokenList = new ArrayList<Token>();
		while (tokenIt.hasNext()) {
			Token t = tokenIt.next();
			tokenList.add(t);
		}
		return tokenList;
	}
	
	/**
	 * retrieves the sentence segmentation data from OpenNLP
	 */
	@SuppressWarnings("unchecked")
	private static List<PlainTextSentenceAnnotation> sentDetect(RelevantText rt){
		// find all sentences that begin inside this relevant text piece
		final Iterator<PlainTextSentenceAnnotation> sentIt = sentIndex.subiterator(rt, true, false);
		List<PlainTextSentenceAnnotation> sentList = new ArrayList<PlainTextSentenceAnnotation>();
		while (sentIt.hasNext()){
			PlainTextSentenceAnnotation s = sentIt.next();
			sentList.add(s);
			//log.debug("sentBegin: " + s.getBegin());
		}
		return sentList;
	}

	/**
	 * converts true => 1 and false => 0.
	 */
	public static int toInt(boolean bool){
		if (bool) return 1;
		else return 0;
	}
	
	/**
	 * uses both == and .equals(_) for equivalence testing (OR-ed).
	 * @return true iff item is in array.
	 */
	public static boolean in(Object item, Object[] array){
		// (cannot be made efficient or replaced with Arrays.binarySearch() 
		// since we need comparison with the equals() method)
		for (Object o : array){
			if (o == item || o.equals(item))
				return true;
		}
		return false;
	}
}
