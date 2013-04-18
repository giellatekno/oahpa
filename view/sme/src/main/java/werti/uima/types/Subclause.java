

/* First created by JCasGen Wed Apr 17 12:34:59 CEST 2013 */
package werti.uima.types;

import org.apache.uima.jcas.JCas; 
import org.apache.uima.jcas.JCasRegistry;
import org.apache.uima.jcas.cas.TOP_Type;

import org.apache.uima.jcas.tcas.Annotation;


/** 
 * Updated by JCasGen Wed Apr 17 12:34:59 CEST 2013
 * XML source: /Users/mslm/view/sme/desc/vislcg3TypeSystem.xml
 * @generated */
public class Subclause extends Annotation {
  /** @generated
   * @ordered 
   */
  public final static int typeIndexID = JCasRegistry.register(Subclause.class);
  /** @generated
   * @ordered 
   */
  public final static int type = typeIndexID;
  /** @generated  */
  public              int getTypeIndexID() {return typeIndexID;}
 
  /** Never called.  Disable default constructor
   * @generated */
  protected Subclause() {}
    
  /** Internal - constructor used by generator 
   * @generated */
  public Subclause(int addr, TOP_Type type) {
    super(addr, type);
    readObject();
  }
  
  /** @generated */
  public Subclause(JCas jcas) {
    super(jcas);
    readObject();   
  } 

  /** @generated */  
  public Subclause(JCas jcas, int begin, int end) {
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
  //* Feature: modifiedSurface

  /** getter for modifiedSurface - gets 
   * @generated */
  public String getModifiedSurface() {
    if (Subclause_Type.featOkTst && ((Subclause_Type)jcasType).casFeat_modifiedSurface == null)
      jcasType.jcas.throwFeatMissing("modifiedSurface", "werti.uima.types.Subclause");
    return jcasType.ll_cas.ll_getStringValue(addr, ((Subclause_Type)jcasType).casFeatCode_modifiedSurface);}
    
  /** setter for modifiedSurface - sets  
   * @generated */
  public void setModifiedSurface(String v) {
    if (Subclause_Type.featOkTst && ((Subclause_Type)jcasType).casFeat_modifiedSurface == null)
      jcasType.jcas.throwFeatMissing("modifiedSurface", "werti.uima.types.Subclause");
    jcasType.ll_cas.ll_setStringValue(addr, ((Subclause_Type)jcasType).casFeatCode_modifiedSurface, v);}    
  }

    