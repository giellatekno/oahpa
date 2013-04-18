

/* First created by JCasGen Wed Apr 17 12:34:59 CEST 2013 */
package werti.uima.types.annot;

import org.apache.uima.jcas.JCas; 
import org.apache.uima.jcas.JCasRegistry;
import org.apache.uima.jcas.cas.TOP_Type;

import org.apache.uima.jcas.cas.FSArray;


/** A token with added Constraint Grammar analysis information.
 * Updated by JCasGen Wed Apr 17 12:34:59 CEST 2013
 * XML source: /Users/mslm/view/sme/desc/vislcg3TypeSystem.xml
 * @generated */
public class CGToken extends Token {
  /** @generated
   * @ordered 
   */
  public final static int typeIndexID = JCasRegistry.register(CGToken.class);
  /** @generated
   * @ordered 
   */
  public final static int type = typeIndexID;
  /** @generated  */
  public              int getTypeIndexID() {return typeIndexID;}
 
  /** Never called.  Disable default constructor
   * @generated */
  protected CGToken() {}
    
  /** Internal - constructor used by generator 
   * @generated */
  public CGToken(int addr, TOP_Type type) {
    super(addr, type);
    readObject();
  }
  
  /** @generated */
  public CGToken(JCas jcas) {
    super(jcas);
    readObject();   
  } 

  /** @generated */  
  public CGToken(JCas jcas, int begin, int end) {
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
  //* Feature: readings

  /** getter for readings - gets A set of readings in this cohort.
   * @generated */
  public FSArray getReadings() {
    if (CGToken_Type.featOkTst && ((CGToken_Type)jcasType).casFeat_readings == null)
      jcasType.jcas.throwFeatMissing("readings", "werti.uima.types.annot.CGToken");
    return (FSArray)(jcasType.ll_cas.ll_getFSForRef(jcasType.ll_cas.ll_getRefValue(addr, ((CGToken_Type)jcasType).casFeatCode_readings)));}
    
  /** setter for readings - sets A set of readings in this cohort. 
   * @generated */
  public void setReadings(FSArray v) {
    if (CGToken_Type.featOkTst && ((CGToken_Type)jcasType).casFeat_readings == null)
      jcasType.jcas.throwFeatMissing("readings", "werti.uima.types.annot.CGToken");
    jcasType.ll_cas.ll_setRefValue(addr, ((CGToken_Type)jcasType).casFeatCode_readings, jcasType.ll_cas.ll_getFSRef(v));}    
    
  /** indexed getter for readings - gets an indexed value - A set of readings in this cohort.
   * @generated */
  public CGReading getReadings(int i) {
    if (CGToken_Type.featOkTst && ((CGToken_Type)jcasType).casFeat_readings == null)
      jcasType.jcas.throwFeatMissing("readings", "werti.uima.types.annot.CGToken");
    jcasType.jcas.checkArrayBounds(jcasType.ll_cas.ll_getRefValue(addr, ((CGToken_Type)jcasType).casFeatCode_readings), i);
    return (CGReading)(jcasType.ll_cas.ll_getFSForRef(jcasType.ll_cas.ll_getRefArrayValue(jcasType.ll_cas.ll_getRefValue(addr, ((CGToken_Type)jcasType).casFeatCode_readings), i)));}

  /** indexed setter for readings - sets an indexed value - A set of readings in this cohort.
   * @generated */
  public void setReadings(int i, CGReading v) { 
    if (CGToken_Type.featOkTst && ((CGToken_Type)jcasType).casFeat_readings == null)
      jcasType.jcas.throwFeatMissing("readings", "werti.uima.types.annot.CGToken");
    jcasType.jcas.checkArrayBounds(jcasType.ll_cas.ll_getRefValue(addr, ((CGToken_Type)jcasType).casFeatCode_readings), i);
    jcasType.ll_cas.ll_setRefArrayValue(jcasType.ll_cas.ll_getRefValue(addr, ((CGToken_Type)jcasType).casFeatCode_readings), i, jcasType.ll_cas.ll_getFSRef(v));}
  }

    