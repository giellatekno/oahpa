
/* First created by JCasGen Wed Apr 17 12:34:59 CEST 2013 */
package werti.uima.types.annot;

import org.apache.uima.jcas.JCas;
import org.apache.uima.jcas.JCasRegistry;
import org.apache.uima.cas.impl.CASImpl;
import org.apache.uima.cas.impl.FSGenerator;
import org.apache.uima.cas.FeatureStructure;
import org.apache.uima.cas.impl.TypeImpl;
import org.apache.uima.cas.Type;
import org.apache.uima.jcas.cas.NonEmptyStringList_Type;

/** A reading in a constraint grammar cohort.
 * Updated by JCasGen Wed Apr 17 12:34:59 CEST 2013
 * @generated */
public class CGReading_Type extends NonEmptyStringList_Type {
  /** @generated */
  protected FSGenerator getFSGenerator() {return fsGenerator;}
  /** @generated */
  private final FSGenerator fsGenerator = 
    new FSGenerator() {
      public FeatureStructure createFS(int addr, CASImpl cas) {
  			 if (CGReading_Type.this.useExistingInstance) {
  			   // Return eq fs instance if already created
  		     FeatureStructure fs = CGReading_Type.this.jcas.getJfsFromCaddr(addr);
  		     if (null == fs) {
  		       fs = new CGReading(addr, CGReading_Type.this);
  			   CGReading_Type.this.jcas.putJfsFromCaddr(addr, fs);
  			   return fs;
  		     }
  		     return fs;
        } else return new CGReading(addr, CGReading_Type.this);
  	  }
    };
  /** @generated */
  public final static int typeIndexID = CGReading.typeIndexID;
  /** @generated 
     @modifiable */
  public final static boolean featOkTst = JCasRegistry.getFeatOkTst("werti.uima.types.annot.CGReading");



  /** initialize variables to correspond with Cas Type and Features
	* @generated */
  public CGReading_Type(JCas jcas, Type casType) {
    super(jcas, casType);
    casImpl.getFSClassRegistry().addGeneratorForType((TypeImpl)this.casType, getFSGenerator());

  }
}



    