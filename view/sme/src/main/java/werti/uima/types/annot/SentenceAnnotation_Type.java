
/* First created by JCasGen Wed Apr 17 12:34:59 CEST 2013 */
package werti.uima.types.annot;

import org.apache.uima.jcas.JCas;
import org.apache.uima.jcas.JCasRegistry;
import org.apache.uima.cas.impl.CASImpl;
import org.apache.uima.cas.impl.FSGenerator;
import org.apache.uima.cas.FeatureStructure;
import org.apache.uima.cas.impl.TypeImpl;
import org.apache.uima.cas.Type;
import org.apache.uima.cas.impl.FeatureImpl;
import org.apache.uima.cas.Feature;
import org.apache.uima.jcas.tcas.Annotation_Type;

/** A sentence in natural language derived from plain text and HTML features.
 * Updated by JCasGen Wed Apr 17 12:34:59 CEST 2013
 * @generated */
public class SentenceAnnotation_Type extends Annotation_Type {
  /** @generated */
  protected FSGenerator getFSGenerator() {return fsGenerator;}
  /** @generated */
  private final FSGenerator fsGenerator = 
    new FSGenerator() {
      public FeatureStructure createFS(int addr, CASImpl cas) {
  			 if (SentenceAnnotation_Type.this.useExistingInstance) {
  			   // Return eq fs instance if already created
  		     FeatureStructure fs = SentenceAnnotation_Type.this.jcas.getJfsFromCaddr(addr);
  		     if (null == fs) {
  		       fs = new SentenceAnnotation(addr, SentenceAnnotation_Type.this);
  			   SentenceAnnotation_Type.this.jcas.putJfsFromCaddr(addr, fs);
  			   return fs;
  		     }
  		     return fs;
        } else return new SentenceAnnotation(addr, SentenceAnnotation_Type.this);
  	  }
    };
  /** @generated */
  public final static int typeIndexID = SentenceAnnotation.typeIndexID;
  /** @generated 
     @modifiable */
  public final static boolean featOkTst = JCasRegistry.getFeatOkTst("werti.uima.types.annot.SentenceAnnotation");
 
  /** @generated */
  final Feature casFeat_coherence;
  /** @generated */
  final int     casFeatCode_coherence;
  /** @generated */ 
  public double getCoherence(int addr) {
        if (featOkTst && casFeat_coherence == null)
      jcas.throwFeatMissing("coherence", "werti.uima.types.annot.SentenceAnnotation");
    return ll_cas.ll_getDoubleValue(addr, casFeatCode_coherence);
  }
  /** @generated */    
  public void setCoherence(int addr, double v) {
        if (featOkTst && casFeat_coherence == null)
      jcas.throwFeatMissing("coherence", "werti.uima.types.annot.SentenceAnnotation");
    ll_cas.ll_setDoubleValue(addr, casFeatCode_coherence, v);}
    
  
 
  /** @generated */
  final Feature casFeat_sexp;
  /** @generated */
  final int     casFeatCode_sexp;
  /** @generated */ 
  public String getSexp(int addr) {
        if (featOkTst && casFeat_sexp == null)
      jcas.throwFeatMissing("sexp", "werti.uima.types.annot.SentenceAnnotation");
    return ll_cas.ll_getStringValue(addr, casFeatCode_sexp);
  }
  /** @generated */    
  public void setSexp(int addr, String v) {
        if (featOkTst && casFeat_sexp == null)
      jcas.throwFeatMissing("sexp", "werti.uima.types.annot.SentenceAnnotation");
    ll_cas.ll_setStringValue(addr, casFeatCode_sexp, v);}
    
  
 
  /** @generated */
  final Feature casFeat_hasdepparse;
  /** @generated */
  final int     casFeatCode_hasdepparse;
  /** @generated */ 
  public boolean getHasdepparse(int addr) {
        if (featOkTst && casFeat_hasdepparse == null)
      jcas.throwFeatMissing("hasdepparse", "werti.uima.types.annot.SentenceAnnotation");
    return ll_cas.ll_getBooleanValue(addr, casFeatCode_hasdepparse);
  }
  /** @generated */    
  public void setHasdepparse(int addr, boolean v) {
        if (featOkTst && casFeat_hasdepparse == null)
      jcas.throwFeatMissing("hasdepparse", "werti.uima.types.annot.SentenceAnnotation");
    ll_cas.ll_setBooleanValue(addr, casFeatCode_hasdepparse, v);}
    
  
 
  /** @generated */
  final Feature casFeat_activeconversion;
  /** @generated */
  final int     casFeatCode_activeconversion;
  /** @generated */ 
  public String getActiveconversion(int addr) {
        if (featOkTst && casFeat_activeconversion == null)
      jcas.throwFeatMissing("activeconversion", "werti.uima.types.annot.SentenceAnnotation");
    return ll_cas.ll_getStringValue(addr, casFeatCode_activeconversion);
  }
  /** @generated */    
  public void setActiveconversion(int addr, String v) {
        if (featOkTst && casFeat_activeconversion == null)
      jcas.throwFeatMissing("activeconversion", "werti.uima.types.annot.SentenceAnnotation");
    ll_cas.ll_setStringValue(addr, casFeatCode_activeconversion, v);}
    
  
 
  /** @generated */
  final Feature casFeat_passiveconversion;
  /** @generated */
  final int     casFeatCode_passiveconversion;
  /** @generated */ 
  public String getPassiveconversion(int addr) {
        if (featOkTst && casFeat_passiveconversion == null)
      jcas.throwFeatMissing("passiveconversion", "werti.uima.types.annot.SentenceAnnotation");
    return ll_cas.ll_getStringValue(addr, casFeatCode_passiveconversion);
  }
  /** @generated */    
  public void setPassiveconversion(int addr, String v) {
        if (featOkTst && casFeat_passiveconversion == null)
      jcas.throwFeatMissing("passiveconversion", "werti.uima.types.annot.SentenceAnnotation");
    ll_cas.ll_setStringValue(addr, casFeatCode_passiveconversion, v);}
    
  
 
  /** @generated */
  final Feature casFeat_graphs_debug;
  /** @generated */
  final int     casFeatCode_graphs_debug;
  /** @generated */ 
  public int getGraphs_debug(int addr) {
        if (featOkTst && casFeat_graphs_debug == null)
      jcas.throwFeatMissing("graphs_debug", "werti.uima.types.annot.SentenceAnnotation");
    return ll_cas.ll_getRefValue(addr, casFeatCode_graphs_debug);
  }
  /** @generated */    
  public void setGraphs_debug(int addr, int v) {
        if (featOkTst && casFeat_graphs_debug == null)
      jcas.throwFeatMissing("graphs_debug", "werti.uima.types.annot.SentenceAnnotation");
    ll_cas.ll_setRefValue(addr, casFeatCode_graphs_debug, v);}
    
  
 
  /** @generated */
  final Feature casFeat_passiveConversionStrategy;
  /** @generated */
  final int     casFeatCode_passiveConversionStrategy;
  /** @generated */ 
  public String getPassiveConversionStrategy(int addr) {
        if (featOkTst && casFeat_passiveConversionStrategy == null)
      jcas.throwFeatMissing("passiveConversionStrategy", "werti.uima.types.annot.SentenceAnnotation");
    return ll_cas.ll_getStringValue(addr, casFeatCode_passiveConversionStrategy);
  }
  /** @generated */    
  public void setPassiveConversionStrategy(int addr, String v) {
        if (featOkTst && casFeat_passiveConversionStrategy == null)
      jcas.throwFeatMissing("passiveConversionStrategy", "werti.uima.types.annot.SentenceAnnotation");
    ll_cas.ll_setStringValue(addr, casFeatCode_passiveConversionStrategy, v);}
    
  
 
  /** @generated */
  final Feature casFeat_parseCandidate;
  /** @generated */
  final int     casFeatCode_parseCandidate;
  /** @generated */ 
  public boolean getParseCandidate(int addr) {
        if (featOkTst && casFeat_parseCandidate == null)
      jcas.throwFeatMissing("parseCandidate", "werti.uima.types.annot.SentenceAnnotation");
    return ll_cas.ll_getBooleanValue(addr, casFeatCode_parseCandidate);
  }
  /** @generated */    
  public void setParseCandidate(int addr, boolean v) {
        if (featOkTst && casFeat_parseCandidate == null)
      jcas.throwFeatMissing("parseCandidate", "werti.uima.types.annot.SentenceAnnotation");
    ll_cas.ll_setBooleanValue(addr, casFeatCode_parseCandidate, v);}
    
  



  /** initialize variables to correspond with Cas Type and Features
	* @generated */
  public SentenceAnnotation_Type(JCas jcas, Type casType) {
    super(jcas, casType);
    casImpl.getFSClassRegistry().addGeneratorForType((TypeImpl)this.casType, getFSGenerator());

 
    casFeat_coherence = jcas.getRequiredFeatureDE(casType, "coherence", "uima.cas.Double", featOkTst);
    casFeatCode_coherence  = (null == casFeat_coherence) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_coherence).getCode();

 
    casFeat_sexp = jcas.getRequiredFeatureDE(casType, "sexp", "uima.cas.String", featOkTst);
    casFeatCode_sexp  = (null == casFeat_sexp) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_sexp).getCode();

 
    casFeat_hasdepparse = jcas.getRequiredFeatureDE(casType, "hasdepparse", "uima.cas.Boolean", featOkTst);
    casFeatCode_hasdepparse  = (null == casFeat_hasdepparse) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_hasdepparse).getCode();

 
    casFeat_activeconversion = jcas.getRequiredFeatureDE(casType, "activeconversion", "uima.cas.String", featOkTst);
    casFeatCode_activeconversion  = (null == casFeat_activeconversion) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_activeconversion).getCode();

 
    casFeat_passiveconversion = jcas.getRequiredFeatureDE(casType, "passiveconversion", "uima.cas.String", featOkTst);
    casFeatCode_passiveconversion  = (null == casFeat_passiveconversion) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_passiveconversion).getCode();

 
    casFeat_graphs_debug = jcas.getRequiredFeatureDE(casType, "graphs_debug", "uima.cas.StringList", featOkTst);
    casFeatCode_graphs_debug  = (null == casFeat_graphs_debug) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_graphs_debug).getCode();

 
    casFeat_passiveConversionStrategy = jcas.getRequiredFeatureDE(casType, "passiveConversionStrategy", "uima.cas.String", featOkTst);
    casFeatCode_passiveConversionStrategy  = (null == casFeat_passiveConversionStrategy) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_passiveConversionStrategy).getCode();

 
    casFeat_parseCandidate = jcas.getRequiredFeatureDE(casType, "parseCandidate", "uima.cas.Boolean", featOkTst);
    casFeatCode_parseCandidate  = (null == casFeat_parseCandidate) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_parseCandidate).getCode();

  }
}



    