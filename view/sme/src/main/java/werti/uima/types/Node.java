

/* First created by JCasGen Wed Apr 17 12:34:59 CEST 2013 */
package werti.uima.types;

import org.apache.uima.jcas.JCas; 
import org.apache.uima.jcas.JCasRegistry;
import org.apache.uima.jcas.cas.TOP_Type;

import org.apache.uima.jcas.cas.FSList;
import org.apache.uima.jcas.cas.TOP;
import werti.uima.types.annot.Token;


/** A node annotation, representing both leaf nodes of a graph, as well as internal nodes.
        Note that this node type can represent n-ary circular graphs, including multiple parent nodes. Any restriction to this, if it is desired, should originate from the implementation.
 * Updated by JCasGen Wed Apr 17 12:34:59 CEST 2013
 * XML source: /Users/mslm/view/sme/desc/vislcg3TypeSystem.xml
 * @generated */
public class Node extends TOP {
  /** @generated
   * @ordered 
   */
  public final static int typeIndexID = JCasRegistry.register(Node.class);
  /** @generated
   * @ordered 
   */
  public final static int type = typeIndexID;
  /** @generated  */
  public              int getTypeIndexID() {return typeIndexID;}
 
  /** Never called.  Disable default constructor
   * @generated */
  protected Node() {}
    
  /** Internal - constructor used by generator 
   * @generated */
  public Node(int addr, TOP_Type type) {
    super(addr, type);
    readObject();
  }
  
  /** @generated */
  public Node(JCas jcas) {
    super(jcas);
    readObject();   
  } 

  /** <!-- begin-user-doc -->
    * Write your own initialization here
    * <!-- end-user-doc -->
  @generated modifiable */
  private void readObject() {}
     
 
    
  //*--------------*
  //* Feature: token

  /** getter for token - gets The token this edge represents, or null. In case this node represents a token, this will be a Token, otherwise null.
   * @generated */
  public Token getToken() {
    if (Node_Type.featOkTst && ((Node_Type)jcasType).casFeat_token == null)
      jcasType.jcas.throwFeatMissing("token", "werti.uima.types.Node");
    return (Token)(jcasType.ll_cas.ll_getFSForRef(jcasType.ll_cas.ll_getRefValue(addr, ((Node_Type)jcasType).casFeatCode_token)));}
    
  /** setter for token - sets The token this edge represents, or null. In case this node represents a token, this will be a Token, otherwise null. 
   * @generated */
  public void setToken(Token v) {
    if (Node_Type.featOkTst && ((Node_Type)jcasType).casFeat_token == null)
      jcasType.jcas.throwFeatMissing("token", "werti.uima.types.Node");
    jcasType.ll_cas.ll_setRefValue(addr, ((Node_Type)jcasType).casFeatCode_token, jcasType.ll_cas.ll_getFSRef(v));}    
   
    
  //*--------------*
  //* Feature: parents

  /** getter for parents - gets A list of edges representing links to the node's parents.
   * @generated */
  public FSList getParents() {
    if (Node_Type.featOkTst && ((Node_Type)jcasType).casFeat_parents == null)
      jcasType.jcas.throwFeatMissing("parents", "werti.uima.types.Node");
    return (FSList)(jcasType.ll_cas.ll_getFSForRef(jcasType.ll_cas.ll_getRefValue(addr, ((Node_Type)jcasType).casFeatCode_parents)));}
    
  /** setter for parents - sets A list of edges representing links to the node's parents. 
   * @generated */
  public void setParents(FSList v) {
    if (Node_Type.featOkTst && ((Node_Type)jcasType).casFeat_parents == null)
      jcasType.jcas.throwFeatMissing("parents", "werti.uima.types.Node");
    jcasType.ll_cas.ll_setRefValue(addr, ((Node_Type)jcasType).casFeatCode_parents, jcasType.ll_cas.ll_getFSRef(v));}    
   
    
  //*--------------*
  //* Feature: children

  /** getter for children - gets A list of edges, representing the node's children.
   * @generated */
  public FSList getChildren() {
    if (Node_Type.featOkTst && ((Node_Type)jcasType).casFeat_children == null)
      jcasType.jcas.throwFeatMissing("children", "werti.uima.types.Node");
    return (FSList)(jcasType.ll_cas.ll_getFSForRef(jcasType.ll_cas.ll_getRefValue(addr, ((Node_Type)jcasType).casFeatCode_children)));}
    
  /** setter for children - sets A list of edges, representing the node's children. 
   * @generated */
  public void setChildren(FSList v) {
    if (Node_Type.featOkTst && ((Node_Type)jcasType).casFeat_children == null)
      jcasType.jcas.throwFeatMissing("children", "werti.uima.types.Node");
    jcasType.ll_cas.ll_setRefValue(addr, ((Node_Type)jcasType).casFeatCode_children, jcasType.ll_cas.ll_getFSRef(v));}    
  }

    