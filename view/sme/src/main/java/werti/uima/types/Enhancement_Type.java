
/* First created by JCasGen Wed Apr 17 12:34:59 CEST 2013 */
package werti.uima.types;

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

/** Describes an enhancment on the current spot.
 * Updated by JCasGen Wed Apr 17 12:34:59 CEST 2013
 * @generated */
public class Enhancement_Type extends Annotation_Type {
  /** @generated */
  protected FSGenerator getFSGenerator() {return fsGenerator;}
  /** @generated */
  private final FSGenerator fsGenerator = 
    new FSGenerator() {
      public FeatureStructure createFS(int addr, CASImpl cas) {
  			 if (Enhancement_Type.this.useExistingInstance) {
  			   // Return eq fs instance if already created
  		     FeatureStructure fs = Enhancement_Type.this.jcas.getJfsFromCaddr(addr);
  		     if (null == fs) {
  		       fs = new Enhancement(addr, Enhancement_Type.this);
  			   Enhancement_Type.this.jcas.putJfsFromCaddr(addr, fs);
  			   return fs;
  		     }
  		     return fs;
        } else return new Enhancement(addr, Enhancement_Type.this);
  	  }
    };
  /** @generated */
  public final static int typeIndexID = Enhancement.typeIndexID;
  /** @generated 
     @modifiable */
  public final static boolean featOkTst = JCasRegistry.getFeatOkTst("werti.uima.types.Enhancement");
 
  /** @generated */
  final Feature casFeat_EnhanceStart;
  /** @generated */
  final int     casFeatCode_EnhanceStart;
  /** @generated */ 
  public String getEnhanceStart(int addr) {
        if (featOkTst && casFeat_EnhanceStart == null)
      jcas.throwFeatMissing("EnhanceStart", "werti.uima.types.Enhancement");
    return ll_cas.ll_getStringValue(addr, casFeatCode_EnhanceStart);
  }
  /** @generated */    
  public void setEnhanceStart(int addr, String v) {
        if (featOkTst && casFeat_EnhanceStart == null)
      jcas.throwFeatMissing("EnhanceStart", "werti.uima.types.Enhancement");
    ll_cas.ll_setStringValue(addr, casFeatCode_EnhanceStart, v);}
    
  
 
  /** @generated */
  final Feature casFeat_EnhanceEnd;
  /** @generated */
  final int     casFeatCode_EnhanceEnd;
  /** @generated */ 
  public String getEnhanceEnd(int addr) {
        if (featOkTst && casFeat_EnhanceEnd == null)
      jcas.throwFeatMissing("EnhanceEnd", "werti.uima.types.Enhancement");
    return ll_cas.ll_getStringValue(addr, casFeatCode_EnhanceEnd);
  }
  /** @generated */    
  public void setEnhanceEnd(int addr, String v) {
        if (featOkTst && casFeat_EnhanceEnd == null)
      jcas.throwFeatMissing("EnhanceEnd", "werti.uima.types.Enhancement");
    ll_cas.ll_setStringValue(addr, casFeatCode_EnhanceEnd, v);}
    
  
 
  /** @generated */
  final Feature casFeat_Relevant;
  /** @generated */
  final int     casFeatCode_Relevant;
  /** @generated */ 
  public boolean getRelevant(int addr) {
        if (featOkTst && casFeat_Relevant == null)
      jcas.throwFeatMissing("Relevant", "werti.uima.types.Enhancement");
    return ll_cas.ll_getBooleanValue(addr, casFeatCode_Relevant);
  }
  /** @generated */    
  public void setRelevant(int addr, boolean v) {
        if (featOkTst && casFeat_Relevant == null)
      jcas.throwFeatMissing("Relevant", "werti.uima.types.Enhancement");
    ll_cas.ll_setBooleanValue(addr, casFeatCode_Relevant, v);}
    
  



  /** initialize variables to correspond with Cas Type and Features
	* @generated */
  public Enhancement_Type(JCas jcas, Type casType) {
    super(jcas, casType);
    casImpl.getFSClassRegistry().addGeneratorForType((TypeImpl)this.casType, getFSGenerator());

 
    casFeat_EnhanceStart = jcas.getRequiredFeatureDE(casType, "EnhanceStart", "uima.cas.String", featOkTst);
    casFeatCode_EnhanceStart  = (null == casFeat_EnhanceStart) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_EnhanceStart).getCode();

 
    casFeat_EnhanceEnd = jcas.getRequiredFeatureDE(casType, "EnhanceEnd", "uima.cas.String", featOkTst);
    casFeatCode_EnhanceEnd  = (null == casFeat_EnhanceEnd) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_EnhanceEnd).getCode();

 
    casFeat_Relevant = jcas.getRequiredFeatureDE(casType, "Relevant", "uima.cas.Boolean", featOkTst);
    casFeatCode_Relevant  = (null == casFeat_Relevant) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_Relevant).getCode();

  }
}



    