

/* First created by JCasGen Wed Apr 17 12:34:59 CEST 2013 */
package werti.uima.types.annot;

import org.apache.uima.jcas.JCas; 
import org.apache.uima.jcas.JCasRegistry;
import org.apache.uima.jcas.cas.TOP_Type;

import org.apache.uima.jcas.cas.FSArray;
import org.apache.uima.jcas.tcas.Annotation;


/** Annotations for phrasal verbs.
 * Updated by JCasGen Wed Apr 17 12:34:59 CEST 2013
 * XML source: /Users/mslm/view/sme/desc/vislcg3TypeSystem.xml
 * @generated */
public class PhrasalVerb extends Annotation {
  /** @generated
   * @ordered 
   */
  public final static int typeIndexID = JCasRegistry.register(PhrasalVerb.class);
  /** @generated
   * @ordered 
   */
  public final static int type = typeIndexID;
  /** @generated  */
  public              int getTypeIndexID() {return typeIndexID;}
 
  /** Never called.  Disable default constructor
   * @generated */
  protected PhrasalVerb() {}
    
  /** Internal - constructor used by generator 
   * @generated */
  public PhrasalVerb(int addr, TOP_Type type) {
    super(addr, type);
    readObject();
  }
  
  /** @generated */
  public PhrasalVerb(JCas jcas) {
    super(jcas);
    readObject();   
  } 

  /** @generated */  
  public PhrasalVerb(JCas jcas, int begin, int end) {
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
  //* Feature: verb

  /** getter for verb - gets The verb part of the phrasal verb.
   * @generated */
  public FSArray getVerb() {
    if (PhrasalVerb_Type.featOkTst && ((PhrasalVerb_Type)jcasType).casFeat_verb == null)
      jcasType.jcas.throwFeatMissing("verb", "werti.uima.types.annot.PhrasalVerb");
    return (FSArray)(jcasType.ll_cas.ll_getFSForRef(jcasType.ll_cas.ll_getRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_verb)));}
    
  /** setter for verb - sets The verb part of the phrasal verb. 
   * @generated */
  public void setVerb(FSArray v) {
    if (PhrasalVerb_Type.featOkTst && ((PhrasalVerb_Type)jcasType).casFeat_verb == null)
      jcasType.jcas.throwFeatMissing("verb", "werti.uima.types.annot.PhrasalVerb");
    jcasType.ll_cas.ll_setRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_verb, jcasType.ll_cas.ll_getFSRef(v));}    
    
  /** indexed getter for verb - gets an indexed value - The verb part of the phrasal verb.
   * @generated */
  public Token getVerb(int i) {
    if (PhrasalVerb_Type.featOkTst && ((PhrasalVerb_Type)jcasType).casFeat_verb == null)
      jcasType.jcas.throwFeatMissing("verb", "werti.uima.types.annot.PhrasalVerb");
    jcasType.jcas.checkArrayBounds(jcasType.ll_cas.ll_getRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_verb), i);
    return (Token)(jcasType.ll_cas.ll_getFSForRef(jcasType.ll_cas.ll_getRefArrayValue(jcasType.ll_cas.ll_getRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_verb), i)));}

  /** indexed setter for verb - sets an indexed value - The verb part of the phrasal verb.
   * @generated */
  public void setVerb(int i, Token v) { 
    if (PhrasalVerb_Type.featOkTst && ((PhrasalVerb_Type)jcasType).casFeat_verb == null)
      jcasType.jcas.throwFeatMissing("verb", "werti.uima.types.annot.PhrasalVerb");
    jcasType.jcas.checkArrayBounds(jcasType.ll_cas.ll_getRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_verb), i);
    jcasType.ll_cas.ll_setRefArrayValue(jcasType.ll_cas.ll_getRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_verb), i, jcasType.ll_cas.ll_getFSRef(v));}
   
    
  //*--------------*
  //* Feature: particle

  /** getter for particle - gets The particle part of the phrasal verb.
   * @generated */
  public FSArray getParticle() {
    if (PhrasalVerb_Type.featOkTst && ((PhrasalVerb_Type)jcasType).casFeat_particle == null)
      jcasType.jcas.throwFeatMissing("particle", "werti.uima.types.annot.PhrasalVerb");
    return (FSArray)(jcasType.ll_cas.ll_getFSForRef(jcasType.ll_cas.ll_getRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_particle)));}
    
  /** setter for particle - sets The particle part of the phrasal verb. 
   * @generated */
  public void setParticle(FSArray v) {
    if (PhrasalVerb_Type.featOkTst && ((PhrasalVerb_Type)jcasType).casFeat_particle == null)
      jcasType.jcas.throwFeatMissing("particle", "werti.uima.types.annot.PhrasalVerb");
    jcasType.ll_cas.ll_setRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_particle, jcasType.ll_cas.ll_getFSRef(v));}    
    
  /** indexed getter for particle - gets an indexed value - The particle part of the phrasal verb.
   * @generated */
  public Token getParticle(int i) {
    if (PhrasalVerb_Type.featOkTst && ((PhrasalVerb_Type)jcasType).casFeat_particle == null)
      jcasType.jcas.throwFeatMissing("particle", "werti.uima.types.annot.PhrasalVerb");
    jcasType.jcas.checkArrayBounds(jcasType.ll_cas.ll_getRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_particle), i);
    return (Token)(jcasType.ll_cas.ll_getFSForRef(jcasType.ll_cas.ll_getRefArrayValue(jcasType.ll_cas.ll_getRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_particle), i)));}

  /** indexed setter for particle - sets an indexed value - The particle part of the phrasal verb.
   * @generated */
  public void setParticle(int i, Token v) { 
    if (PhrasalVerb_Type.featOkTst && ((PhrasalVerb_Type)jcasType).casFeat_particle == null)
      jcasType.jcas.throwFeatMissing("particle", "werti.uima.types.annot.PhrasalVerb");
    jcasType.jcas.checkArrayBounds(jcasType.ll_cas.ll_getRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_particle), i);
    jcasType.ll_cas.ll_setRefArrayValue(jcasType.ll_cas.ll_getRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_particle), i, jcasType.ll_cas.ll_getFSRef(v));}
   
    
  //*--------------*
  //* Feature: np

  /** getter for np - gets The associated NP part for some phrasal verbs.
   * @generated */
  public FSArray getNp() {
    if (PhrasalVerb_Type.featOkTst && ((PhrasalVerb_Type)jcasType).casFeat_np == null)
      jcasType.jcas.throwFeatMissing("np", "werti.uima.types.annot.PhrasalVerb");
    return (FSArray)(jcasType.ll_cas.ll_getFSForRef(jcasType.ll_cas.ll_getRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_np)));}
    
  /** setter for np - sets The associated NP part for some phrasal verbs. 
   * @generated */
  public void setNp(FSArray v) {
    if (PhrasalVerb_Type.featOkTst && ((PhrasalVerb_Type)jcasType).casFeat_np == null)
      jcasType.jcas.throwFeatMissing("np", "werti.uima.types.annot.PhrasalVerb");
    jcasType.ll_cas.ll_setRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_np, jcasType.ll_cas.ll_getFSRef(v));}    
    
  /** indexed getter for np - gets an indexed value - The associated NP part for some phrasal verbs.
   * @generated */
  public Token getNp(int i) {
    if (PhrasalVerb_Type.featOkTst && ((PhrasalVerb_Type)jcasType).casFeat_np == null)
      jcasType.jcas.throwFeatMissing("np", "werti.uima.types.annot.PhrasalVerb");
    jcasType.jcas.checkArrayBounds(jcasType.ll_cas.ll_getRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_np), i);
    return (Token)(jcasType.ll_cas.ll_getFSForRef(jcasType.ll_cas.ll_getRefArrayValue(jcasType.ll_cas.ll_getRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_np), i)));}

  /** indexed setter for np - sets an indexed value - The associated NP part for some phrasal verbs.
   * @generated */
  public void setNp(int i, Token v) { 
    if (PhrasalVerb_Type.featOkTst && ((PhrasalVerb_Type)jcasType).casFeat_np == null)
      jcasType.jcas.throwFeatMissing("np", "werti.uima.types.annot.PhrasalVerb");
    jcasType.jcas.checkArrayBounds(jcasType.ll_cas.ll_getRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_np), i);
    jcasType.ll_cas.ll_setRefArrayValue(jcasType.ll_cas.ll_getRefValue(addr, ((PhrasalVerb_Type)jcasType).casFeatCode_np), i, jcasType.ll_cas.ll_getFSRef(v));}
  }

    