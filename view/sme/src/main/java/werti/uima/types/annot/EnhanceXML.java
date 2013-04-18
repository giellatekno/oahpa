

/* First created by JCasGen Wed Apr 17 12:34:59 CEST 2013 */
package werti.uima.types.annot;

import org.apache.uima.jcas.JCas; 
import org.apache.uima.jcas.JCasRegistry;
import org.apache.uima.jcas.cas.TOP_Type;

import org.apache.uima.jcas.tcas.Annotation;


/** Annotation spanning an <enhance></enhance> tag.
 * Updated by JCasGen Wed Apr 17 12:34:59 CEST 2013
 * XML source: /Users/mslm/view/sme/desc/vislcg3TypeSystem.xml
 * @generated */
public class EnhanceXML extends Annotation {
  /** @generated
   * @ordered 
   */
  public final static int typeIndexID = JCasRegistry.register(EnhanceXML.class);
  /** @generated
   * @ordered 
   */
  public final static int type = typeIndexID;
  /** @generated  */
  public              int getTypeIndexID() {return typeIndexID;}
 
  /** Never called.  Disable default constructor
   * @generated */
  protected EnhanceXML() {}
    
  /** Internal - constructor used by generator 
   * @generated */
  public EnhanceXML(int addr, TOP_Type type) {
    super(addr, type);
    readObject();
  }
  
  /** @generated */
  public EnhanceXML(JCas jcas) {
    super(jcas);
    readObject();   
  } 

  /** @generated */  
  public EnhanceXML(JCas jcas, int begin, int end) {
    super(jcas);
    setBegin(begin);
    setEnd(end);
    readObject();
  }   

  /** <!-- begin-user-doc -->
    * Write your own initialization here
    * <!-- end-user-doc -->
  @generated modifiable */
  private void readObject() {}
     
 
    
  //*--------------*
  //* Feature: tag_name

  /** getter for tag_name - gets The name of the tag.
   * @generated */
  public String getTag_name() {
    if (EnhanceXML_Type.featOkTst && ((EnhanceXML_Type)jcasType).casFeat_tag_name == null)
      jcasType.jcas.throwFeatMissing("tag_name", "werti.uima.types.annot.EnhanceXML");
    return jcasType.ll_cas.ll_getStringValue(addr, ((EnhanceXML_Type)jcasType).casFeatCode_tag_name);}
    
  /** setter for tag_name - sets The name of the tag. 
   * @generated */
  public void setTag_name(String v) {
    if (EnhanceXML_Type.featOkTst && ((EnhanceXML_Type)jcasType).casFeat_tag_name == null)
      jcasType.jcas.throwFeatMissing("tag_name", "werti.uima.types.annot.EnhanceXML");
    jcasType.ll_cas.ll_setStringValue(addr, ((EnhanceXML_Type)jcasType).casFeatCode_tag_name, v);}    
   
    
  //*--------------*
  //* Feature: closing

  /** getter for closing - gets Is this tag closing?
   * @generated */
  public boolean getClosing() {
    if (EnhanceXML_Type.featOkTst && ((EnhanceXML_Type)jcasType).casFeat_closing == null)
      jcasType.jcas.throwFeatMissing("closing", "werti.uima.types.annot.EnhanceXML");
    return jcasType.ll_cas.ll_getBooleanValue(addr, ((EnhanceXML_Type)jcasType).casFeatCode_closing);}
    
  /** setter for closing - sets Is this tag closing? 
   * @generated */
  public void setClosing(boolean v) {
    if (EnhanceXML_Type.featOkTst && ((EnhanceXML_Type)jcasType).casFeat_closing == null)
      jcasType.jcas.throwFeatMissing("closing", "werti.uima.types.annot.EnhanceXML");
    jcasType.ll_cas.ll_setBooleanValue(addr, ((EnhanceXML_Type)jcasType).casFeatCode_closing, v);}    
   
    
  //*--------------*
  //* Feature: irrelevant

  /** getter for irrelevant - gets Is this a tag irrelevant to the interpreter? (like script, functional comment tags...)
   * @generated */
  public boolean getIrrelevant() {
    if (EnhanceXML_Type.featOkTst && ((EnhanceXML_Type)jcasType).casFeat_irrelevant == null)
      jcasType.jcas.throwFeatMissing("irrelevant", "werti.uima.types.annot.EnhanceXML");
    return jcasType.ll_cas.ll_getBooleanValue(addr, ((EnhanceXML_Type)jcasType).casFeatCode_irrelevant);}
    
  /** setter for irrelevant - sets Is this a tag irrelevant to the interpreter? (like script, functional comment tags...) 
   * @generated */
  public void setIrrelevant(boolean v) {
    if (EnhanceXML_Type.featOkTst && ((EnhanceXML_Type)jcasType).casFeat_irrelevant == null)
      jcasType.jcas.throwFeatMissing("irrelevant", "werti.uima.types.annot.EnhanceXML");
    jcasType.ll_cas.ll_setBooleanValue(addr, ((EnhanceXML_Type)jcasType).casFeatCode_irrelevant, v);}    
  }

    