
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

/** 
 * Updated by JCasGen Wed Apr 17 12:34:59 CEST 2013
 * @generated */
public class Subclause_Type extends Annotation_Type {
  /** @generated */
  protected FSGenerator getFSGenerator() {return fsGenerator;}
  /** @generated */
  private final FSGenerator fsGenerator = 
    new FSGenerator() {
      public FeatureStructure createFS(int addr, CASImpl cas) {
  			 if (Subclause_Type.this.useExistingInstance) {
  			   // Return eq fs instance if already created
  		     FeatureStructure fs = Subclause_Type.this.jcas.getJfsFromCaddr(addr);
  		     if (null == fs) {
  		       fs = new Subclause(addr, Subclause_Type.this);
  			   Subclause_Type.this.jcas.putJfsFromCaddr(addr, fs);
  			   return fs;
  		     }
  		     return fs;
        } else return new Subclause(addr, Subclause_Type.this);
  	  }
    };
  /** @generated */
  public final static int typeIndexID = Subclause.typeIndexID;
  /** @generated 
     @modifiable */
  public final static boolean featOkTst = JCasRegistry.getFeatOkTst("werti.uima.types.Subclause");
 
  /** @generated */
  final Feature casFeat_modifiedSurface;
  /** @generated */
  final int     casFeatCode_modifiedSurface;
  /** @generated */ 
  public String getModifiedSurface(int addr) {
        if (featOkTst && casFeat_modifiedSurface == null)
      jcas.throwFeatMissing("modifiedSurface", "werti.uima.types.Subclause");
    return ll_cas.ll_getStringValue(addr, casFeatCode_modifiedSurface);
  }
  /** @generated */    
  public void setModifiedSurface(int addr, String v) {
        if (featOkTst && casFeat_modifiedSurface == null)
      jcas.throwFeatMissing("modifiedSurface", "werti.uima.types.Subclause");
    ll_cas.ll_setStringValue(addr, casFeatCode_modifiedSurface, v);}
    
  



  /** initialize variables to correspond with Cas Type and Features
	* @generated */
  public Subclause_Type(JCas jcas, Type casType) {
    super(jcas, casType);
    casImpl.getFSClassRegistry().addGeneratorForType((TypeImpl)this.casType, getFSGenerator());

 
    casFeat_modifiedSurface = jcas.getRequiredFeatureDE(casType, "modifiedSurface", "uima.cas.String", featOkTst);
    casFeatCode_modifiedSurface  = (null == casFeat_modifiedSurface) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_modifiedSurface).getCode();

  }
}



    