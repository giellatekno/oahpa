
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
import org.apache.uima.jcas.cas.TOP_Type;

/** Marks a unidirectional edge in a graph. Only the target node is represented, and the name. Edges are supposed to be fields of nodes.
 * Updated by JCasGen Wed Apr 17 12:34:59 CEST 2013
 * @generated */
public class Edge_Type extends TOP_Type {
  /** @generated */
  protected FSGenerator getFSGenerator() {return fsGenerator;}
  /** @generated */
  private final FSGenerator fsGenerator = 
    new FSGenerator() {
      public FeatureStructure createFS(int addr, CASImpl cas) {
  			 if (Edge_Type.this.useExistingInstance) {
  			   // Return eq fs instance if already created
  		     FeatureStructure fs = Edge_Type.this.jcas.getJfsFromCaddr(addr);
  		     if (null == fs) {
  		       fs = new Edge(addr, Edge_Type.this);
  			   Edge_Type.this.jcas.putJfsFromCaddr(addr, fs);
  			   return fs;
  		     }
  		     return fs;
        } else return new Edge(addr, Edge_Type.this);
  	  }
    };
  /** @generated */
  public final static int typeIndexID = Edge.typeIndexID;
  /** @generated 
     @modifiable */
  public final static boolean featOkTst = JCasRegistry.getFeatOkTst("werti.uima.types.Edge");
 
  /** @generated */
  final Feature casFeat_label;
  /** @generated */
  final int     casFeatCode_label;
  /** @generated */ 
  public String getLabel(int addr) {
        if (featOkTst && casFeat_label == null)
      jcas.throwFeatMissing("label", "werti.uima.types.Edge");
    return ll_cas.ll_getStringValue(addr, casFeatCode_label);
  }
  /** @generated */    
  public void setLabel(int addr, String v) {
        if (featOkTst && casFeat_label == null)
      jcas.throwFeatMissing("label", "werti.uima.types.Edge");
    ll_cas.ll_setStringValue(addr, casFeatCode_label, v);}
    
  
 
  /** @generated */
  final Feature casFeat_target;
  /** @generated */
  final int     casFeatCode_target;
  /** @generated */ 
  public int getTarget(int addr) {
        if (featOkTst && casFeat_target == null)
      jcas.throwFeatMissing("target", "werti.uima.types.Edge");
    return ll_cas.ll_getRefValue(addr, casFeatCode_target);
  }
  /** @generated */    
  public void setTarget(int addr, int v) {
        if (featOkTst && casFeat_target == null)
      jcas.throwFeatMissing("target", "werti.uima.types.Edge");
    ll_cas.ll_setRefValue(addr, casFeatCode_target, v);}
    
  



  /** initialize variables to correspond with Cas Type and Features
	* @generated */
  public Edge_Type(JCas jcas, Type casType) {
    super(jcas, casType);
    casImpl.getFSClassRegistry().addGeneratorForType((TypeImpl)this.casType, getFSGenerator());

 
    casFeat_label = jcas.getRequiredFeatureDE(casType, "label", "uima.cas.String", featOkTst);
    casFeatCode_label  = (null == casFeat_label) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_label).getCode();

 
    casFeat_target = jcas.getRequiredFeatureDE(casType, "target", "werti.uima.types.Node", featOkTst);
    casFeatCode_target  = (null == casFeat_target) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_target).getCode();

  }
}



    