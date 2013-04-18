
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

/** Annotation spanning an <enhance></enhance> tag.
 * Updated by JCasGen Wed Apr 17 12:34:59 CEST 2013
 * @generated */
public class EnhanceXML_Type extends Annotation_Type {
  /** @generated */
  protected FSGenerator getFSGenerator() {return fsGenerator;}
  /** @generated */
  private final FSGenerator fsGenerator = 
    new FSGenerator() {
      public FeatureStructure createFS(int addr, CASImpl cas) {
  			 if (EnhanceXML_Type.this.useExistingInstance) {
  			   // Return eq fs instance if already created
  		     FeatureStructure fs = EnhanceXML_Type.this.jcas.getJfsFromCaddr(addr);
  		     if (null == fs) {
  		       fs = new EnhanceXML(addr, EnhanceXML_Type.this);
  			   EnhanceXML_Type.this.jcas.putJfsFromCaddr(addr, fs);
  			   return fs;
  		     }
  		     return fs;
        } else return new EnhanceXML(addr, EnhanceXML_Type.this);
  	  }
    };
  /** @generated */
  public final static int typeIndexID = EnhanceXML.typeIndexID;
  /** @generated 
     @modifiable */
  public final static boolean featOkTst = JCasRegistry.getFeatOkTst("werti.uima.types.annot.EnhanceXML");
 
  /** @generated */
  final Feature casFeat_tag_name;
  /** @generated */
  final int     casFeatCode_tag_name;
  /** @generated */ 
  public String getTag_name(int addr) {
        if (featOkTst && casFeat_tag_name == null)
      jcas.throwFeatMissing("tag_name", "werti.uima.types.annot.EnhanceXML");
    return ll_cas.ll_getStringValue(addr, casFeatCode_tag_name);
  }
  /** @generated */    
  public void setTag_name(int addr, String v) {
        if (featOkTst && casFeat_tag_name == null)
      jcas.throwFeatMissing("tag_name", "werti.uima.types.annot.EnhanceXML");
    ll_cas.ll_setStringValue(addr, casFeatCode_tag_name, v);}
    
  
 
  /** @generated */
  final Feature casFeat_closing;
  /** @generated */
  final int     casFeatCode_closing;
  /** @generated */ 
  public boolean getClosing(int addr) {
        if (featOkTst && casFeat_closing == null)
      jcas.throwFeatMissing("closing", "werti.uima.types.annot.EnhanceXML");
    return ll_cas.ll_getBooleanValue(addr, casFeatCode_closing);
  }
  /** @generated */    
  public void setClosing(int addr, boolean v) {
        if (featOkTst && casFeat_closing == null)
      jcas.throwFeatMissing("closing", "werti.uima.types.annot.EnhanceXML");
    ll_cas.ll_setBooleanValue(addr, casFeatCode_closing, v);}
    
  
 
  /** @generated */
  final Feature casFeat_irrelevant;
  /** @generated */
  final int     casFeatCode_irrelevant;
  /** @generated */ 
  public boolean getIrrelevant(int addr) {
        if (featOkTst && casFeat_irrelevant == null)
      jcas.throwFeatMissing("irrelevant", "werti.uima.types.annot.EnhanceXML");
    return ll_cas.ll_getBooleanValue(addr, casFeatCode_irrelevant);
  }
  /** @generated */    
  public void setIrrelevant(int addr, boolean v) {
        if (featOkTst && casFeat_irrelevant == null)
      jcas.throwFeatMissing("irrelevant", "werti.uima.types.annot.EnhanceXML");
    ll_cas.ll_setBooleanValue(addr, casFeatCode_irrelevant, v);}
    
  



  /** initialize variables to correspond with Cas Type and Features
	* @generated */
  public EnhanceXML_Type(JCas jcas, Type casType) {
    super(jcas, casType);
    casImpl.getFSClassRegistry().addGeneratorForType((TypeImpl)this.casType, getFSGenerator());

 
    casFeat_tag_name = jcas.getRequiredFeatureDE(casType, "tag_name", "uima.cas.String", featOkTst);
    casFeatCode_tag_name  = (null == casFeat_tag_name) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_tag_name).getCode();

 
    casFeat_closing = jcas.getRequiredFeatureDE(casType, "closing", "uima.cas.Boolean", featOkTst);
    casFeatCode_closing  = (null == casFeat_closing) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_closing).getCode();

 
    casFeat_irrelevant = jcas.getRequiredFeatureDE(casType, "irrelevant", "uima.cas.Boolean", featOkTst);
    casFeatCode_irrelevant  = (null == casFeat_irrelevant) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_irrelevant).getCode();

  }
}



    