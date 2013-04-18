
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

/** A token with added Constraint Grammar analysis information.
 * Updated by JCasGen Wed Apr 17 12:34:59 CEST 2013
 * @generated */
public class CGToken_Type extends Token_Type {
  /** @generated */
  protected FSGenerator getFSGenerator() {return fsGenerator;}
  /** @generated */
  private final FSGenerator fsGenerator = 
    new FSGenerator() {
      public FeatureStructure createFS(int addr, CASImpl cas) {
  			 if (CGToken_Type.this.useExistingInstance) {
  			   // Return eq fs instance if already created
  		     FeatureStructure fs = CGToken_Type.this.jcas.getJfsFromCaddr(addr);
  		     if (null == fs) {
  		       fs = new CGToken(addr, CGToken_Type.this);
  			   CGToken_Type.this.jcas.putJfsFromCaddr(addr, fs);
  			   return fs;
  		     }
  		     return fs;
        } else return new CGToken(addr, CGToken_Type.this);
  	  }
    };
  /** @generated */
  public final static int typeIndexID = CGToken.typeIndexID;
  /** @generated 
     @modifiable */
  public final static boolean featOkTst = JCasRegistry.getFeatOkTst("werti.uima.types.annot.CGToken");
 
  /** @generated */
  final Feature casFeat_readings;
  /** @generated */
  final int     casFeatCode_readings;
  /** @generated */ 
  public int getReadings(int addr) {
        if (featOkTst && casFeat_readings == null)
      jcas.throwFeatMissing("readings", "werti.uima.types.annot.CGToken");
    return ll_cas.ll_getRefValue(addr, casFeatCode_readings);
  }
  /** @generated */    
  public void setReadings(int addr, int v) {
        if (featOkTst && casFeat_readings == null)
      jcas.throwFeatMissing("readings", "werti.uima.types.annot.CGToken");
    ll_cas.ll_setRefValue(addr, casFeatCode_readings, v);}
    
   /** @generated */
  public int getReadings(int addr, int i) {
        if (featOkTst && casFeat_readings == null)
      jcas.throwFeatMissing("readings", "werti.uima.types.annot.CGToken");
    if (lowLevelTypeChecks)
      return ll_cas.ll_getRefArrayValue(ll_cas.ll_getRefValue(addr, casFeatCode_readings), i, true);
    jcas.checkArrayBounds(ll_cas.ll_getRefValue(addr, casFeatCode_readings), i);
	return ll_cas.ll_getRefArrayValue(ll_cas.ll_getRefValue(addr, casFeatCode_readings), i);
  }
   
  /** @generated */ 
  public void setReadings(int addr, int i, int v) {
        if (featOkTst && casFeat_readings == null)
      jcas.throwFeatMissing("readings", "werti.uima.types.annot.CGToken");
    if (lowLevelTypeChecks)
      ll_cas.ll_setRefArrayValue(ll_cas.ll_getRefValue(addr, casFeatCode_readings), i, v, true);
    jcas.checkArrayBounds(ll_cas.ll_getRefValue(addr, casFeatCode_readings), i);
    ll_cas.ll_setRefArrayValue(ll_cas.ll_getRefValue(addr, casFeatCode_readings), i, v);
  }
 



  /** initialize variables to correspond with Cas Type and Features
	* @generated */
  public CGToken_Type(JCas jcas, Type casType) {
    super(jcas, casType);
    casImpl.getFSClassRegistry().addGeneratorForType((TypeImpl)this.casType, getFSGenerator());

 
    casFeat_readings = jcas.getRequiredFeatureDE(casType, "readings", "uima.cas.FSArray", featOkTst);
    casFeatCode_readings  = (null == casFeat_readings) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_readings).getCode();

  }
}



    