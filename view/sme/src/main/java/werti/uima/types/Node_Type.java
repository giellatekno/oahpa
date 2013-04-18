
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

/** A node annotation, representing both leaf nodes of a graph, as well as internal nodes.
        Note that this node type can represent n-ary circular graphs, including multiple parent nodes. Any restriction to this, if it is desired, should originate from the implementation.
 * Updated by JCasGen Wed Apr 17 12:34:59 CEST 2013
 * @generated */
public class Node_Type extends TOP_Type {
  /** @generated */
  protected FSGenerator getFSGenerator() {return fsGenerator;}
  /** @generated */
  private final FSGenerator fsGenerator = 
    new FSGenerator() {
      public FeatureStructure createFS(int addr, CASImpl cas) {
  			 if (Node_Type.this.useExistingInstance) {
  			   // Return eq fs instance if already created
  		     FeatureStructure fs = Node_Type.this.jcas.getJfsFromCaddr(addr);
  		     if (null == fs) {
  		       fs = new Node(addr, Node_Type.this);
  			   Node_Type.this.jcas.putJfsFromCaddr(addr, fs);
  			   return fs;
  		     }
  		     return fs;
        } else return new Node(addr, Node_Type.this);
  	  }
    };
  /** @generated */
  public final static int typeIndexID = Node.typeIndexID;
  /** @generated 
     @modifiable */
  public final static boolean featOkTst = JCasRegistry.getFeatOkTst("werti.uima.types.Node");
 
  /** @generated */
  final Feature casFeat_token;
  /** @generated */
  final int     casFeatCode_token;
  /** @generated */ 
  public int getToken(int addr) {
        if (featOkTst && casFeat_token == null)
      jcas.throwFeatMissing("token", "werti.uima.types.Node");
    return ll_cas.ll_getRefValue(addr, casFeatCode_token);
  }
  /** @generated */    
  public void setToken(int addr, int v) {
        if (featOkTst && casFeat_token == null)
      jcas.throwFeatMissing("token", "werti.uima.types.Node");
    ll_cas.ll_setRefValue(addr, casFeatCode_token, v);}
    
  
 
  /** @generated */
  final Feature casFeat_parents;
  /** @generated */
  final int     casFeatCode_parents;
  /** @generated */ 
  public int getParents(int addr) {
        if (featOkTst && casFeat_parents == null)
      jcas.throwFeatMissing("parents", "werti.uima.types.Node");
    return ll_cas.ll_getRefValue(addr, casFeatCode_parents);
  }
  /** @generated */    
  public void setParents(int addr, int v) {
        if (featOkTst && casFeat_parents == null)
      jcas.throwFeatMissing("parents", "werti.uima.types.Node");
    ll_cas.ll_setRefValue(addr, casFeatCode_parents, v);}
    
  
 
  /** @generated */
  final Feature casFeat_children;
  /** @generated */
  final int     casFeatCode_children;
  /** @generated */ 
  public int getChildren(int addr) {
        if (featOkTst && casFeat_children == null)
      jcas.throwFeatMissing("children", "werti.uima.types.Node");
    return ll_cas.ll_getRefValue(addr, casFeatCode_children);
  }
  /** @generated */    
  public void setChildren(int addr, int v) {
        if (featOkTst && casFeat_children == null)
      jcas.throwFeatMissing("children", "werti.uima.types.Node");
    ll_cas.ll_setRefValue(addr, casFeatCode_children, v);}
    
  



  /** initialize variables to correspond with Cas Type and Features
	* @generated */
  public Node_Type(JCas jcas, Type casType) {
    super(jcas, casType);
    casImpl.getFSClassRegistry().addGeneratorForType((TypeImpl)this.casType, getFSGenerator());

 
    casFeat_token = jcas.getRequiredFeatureDE(casType, "token", "werti.uima.types.annot.Token", featOkTst);
    casFeatCode_token  = (null == casFeat_token) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_token).getCode();

 
    casFeat_parents = jcas.getRequiredFeatureDE(casType, "parents", "uima.cas.FSList", featOkTst);
    casFeatCode_parents  = (null == casFeat_parents) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_parents).getCode();

 
    casFeat_children = jcas.getRequiredFeatureDE(casType, "children", "uima.cas.FSList", featOkTst);
    casFeatCode_children  = (null == casFeat_children) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_children).getCode();

  }
}



    