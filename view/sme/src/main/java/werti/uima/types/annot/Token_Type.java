
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

/** A relevant Token with PoS information attached.
 * Updated by JCasGen Wed Apr 17 12:34:59 CEST 2013
 * @generated */
public class Token_Type extends Annotation_Type {
  /** @generated */
  protected FSGenerator getFSGenerator() {return fsGenerator;}
  /** @generated */
  private final FSGenerator fsGenerator = 
    new FSGenerator() {
      public FeatureStructure createFS(int addr, CASImpl cas) {
  			 if (Token_Type.this.useExistingInstance) {
  			   // Return eq fs instance if already created
  		     FeatureStructure fs = Token_Type.this.jcas.getJfsFromCaddr(addr);
  		     if (null == fs) {
  		       fs = new Token(addr, Token_Type.this);
  			   Token_Type.this.jcas.putJfsFromCaddr(addr, fs);
  			   return fs;
  		     }
  		     return fs;
        } else return new Token(addr, Token_Type.this);
  	  }
    };
  /** @generated */
  public final static int typeIndexID = Token.typeIndexID;
  /** @generated 
     @modifiable */
  public final static boolean featOkTst = JCasRegistry.getFeatOkTst("werti.uima.types.annot.Token");
 
  /** @generated */
  final Feature casFeat_tag;
  /** @generated */
  final int     casFeatCode_tag;
  /** @generated */ 
  public String getTag(int addr) {
        if (featOkTst && casFeat_tag == null)
      jcas.throwFeatMissing("tag", "werti.uima.types.annot.Token");
    return ll_cas.ll_getStringValue(addr, casFeatCode_tag);
  }
  /** @generated */    
  public void setTag(int addr, String v) {
        if (featOkTst && casFeat_tag == null)
      jcas.throwFeatMissing("tag", "werti.uima.types.annot.Token");
    ll_cas.ll_setStringValue(addr, casFeatCode_tag, v);}
    
  
 
  /** @generated */
  final Feature casFeat_detailedtag;
  /** @generated */
  final int     casFeatCode_detailedtag;
  /** @generated */ 
  public String getDetailedtag(int addr) {
        if (featOkTst && casFeat_detailedtag == null)
      jcas.throwFeatMissing("detailedtag", "werti.uima.types.annot.Token");
    return ll_cas.ll_getStringValue(addr, casFeatCode_detailedtag);
  }
  /** @generated */    
  public void setDetailedtag(int addr, String v) {
        if (featOkTst && casFeat_detailedtag == null)
      jcas.throwFeatMissing("detailedtag", "werti.uima.types.annot.Token");
    ll_cas.ll_setStringValue(addr, casFeatCode_detailedtag, v);}
    
  
 
  /** @generated */
  final Feature casFeat_lemma;
  /** @generated */
  final int     casFeatCode_lemma;
  /** @generated */ 
  public String getLemma(int addr) {
        if (featOkTst && casFeat_lemma == null)
      jcas.throwFeatMissing("lemma", "werti.uima.types.annot.Token");
    return ll_cas.ll_getStringValue(addr, casFeatCode_lemma);
  }
  /** @generated */    
  public void setLemma(int addr, String v) {
        if (featOkTst && casFeat_lemma == null)
      jcas.throwFeatMissing("lemma", "werti.uima.types.annot.Token");
    ll_cas.ll_setStringValue(addr, casFeatCode_lemma, v);}
    
  
 
  /** @generated */
  final Feature casFeat_gerund;
  /** @generated */
  final int     casFeatCode_gerund;
  /** @generated */ 
  public String getGerund(int addr) {
        if (featOkTst && casFeat_gerund == null)
      jcas.throwFeatMissing("gerund", "werti.uima.types.annot.Token");
    return ll_cas.ll_getStringValue(addr, casFeatCode_gerund);
  }
  /** @generated */    
  public void setGerund(int addr, String v) {
        if (featOkTst && casFeat_gerund == null)
      jcas.throwFeatMissing("gerund", "werti.uima.types.annot.Token");
    ll_cas.ll_setStringValue(addr, casFeatCode_gerund, v);}
    
  
 
  /** @generated */
  final Feature casFeat_chunk;
  /** @generated */
  final int     casFeatCode_chunk;
  /** @generated */ 
  public String getChunk(int addr) {
        if (featOkTst && casFeat_chunk == null)
      jcas.throwFeatMissing("chunk", "werti.uima.types.annot.Token");
    return ll_cas.ll_getStringValue(addr, casFeatCode_chunk);
  }
  /** @generated */    
  public void setChunk(int addr, String v) {
        if (featOkTst && casFeat_chunk == null)
      jcas.throwFeatMissing("chunk", "werti.uima.types.annot.Token");
    ll_cas.ll_setStringValue(addr, casFeatCode_chunk, v);}
    
  
 
  /** @generated */
  final Feature casFeat_mltag;
  /** @generated */
  final int     casFeatCode_mltag;
  /** @generated */ 
  public String getMltag(int addr) {
        if (featOkTst && casFeat_mltag == null)
      jcas.throwFeatMissing("mltag", "werti.uima.types.annot.Token");
    return ll_cas.ll_getStringValue(addr, casFeatCode_mltag);
  }
  /** @generated */    
  public void setMltag(int addr, String v) {
        if (featOkTst && casFeat_mltag == null)
      jcas.throwFeatMissing("mltag", "werti.uima.types.annot.Token");
    ll_cas.ll_setStringValue(addr, casFeatCode_mltag, v);}
    
  
 
  /** @generated */
  final Feature casFeat_depid;
  /** @generated */
  final int     casFeatCode_depid;
  /** @generated */ 
  public int getDepid(int addr) {
        if (featOkTst && casFeat_depid == null)
      jcas.throwFeatMissing("depid", "werti.uima.types.annot.Token");
    return ll_cas.ll_getIntValue(addr, casFeatCode_depid);
  }
  /** @generated */    
  public void setDepid(int addr, int v) {
        if (featOkTst && casFeat_depid == null)
      jcas.throwFeatMissing("depid", "werti.uima.types.annot.Token");
    ll_cas.ll_setIntValue(addr, casFeatCode_depid, v);}
    
  
 
  /** @generated */
  final Feature casFeat_dephead;
  /** @generated */
  final int     casFeatCode_dephead;
  /** @generated */ 
  public int getDephead(int addr) {
        if (featOkTst && casFeat_dephead == null)
      jcas.throwFeatMissing("dephead", "werti.uima.types.annot.Token");
    return ll_cas.ll_getIntValue(addr, casFeatCode_dephead);
  }
  /** @generated */    
  public void setDephead(int addr, int v) {
        if (featOkTst && casFeat_dephead == null)
      jcas.throwFeatMissing("dephead", "werti.uima.types.annot.Token");
    ll_cas.ll_setIntValue(addr, casFeatCode_dephead, v);}
    
  
 
  /** @generated */
  final Feature casFeat_deprel;
  /** @generated */
  final int     casFeatCode_deprel;
  /** @generated */ 
  public String getDeprel(int addr) {
        if (featOkTst && casFeat_deprel == null)
      jcas.throwFeatMissing("deprel", "werti.uima.types.annot.Token");
    return ll_cas.ll_getStringValue(addr, casFeatCode_deprel);
  }
  /** @generated */    
  public void setDeprel(int addr, String v) {
        if (featOkTst && casFeat_deprel == null)
      jcas.throwFeatMissing("deprel", "werti.uima.types.annot.Token");
    ll_cas.ll_setStringValue(addr, casFeatCode_deprel, v);}
    
  
 
  /** @generated */
  final Feature casFeat_maltdepid;
  /** @generated */
  final int     casFeatCode_maltdepid;
  /** @generated */ 
  public int getMaltdepid(int addr) {
        if (featOkTst && casFeat_maltdepid == null)
      jcas.throwFeatMissing("maltdepid", "werti.uima.types.annot.Token");
    return ll_cas.ll_getIntValue(addr, casFeatCode_maltdepid);
  }
  /** @generated */    
  public void setMaltdepid(int addr, int v) {
        if (featOkTst && casFeat_maltdepid == null)
      jcas.throwFeatMissing("maltdepid", "werti.uima.types.annot.Token");
    ll_cas.ll_setIntValue(addr, casFeatCode_maltdepid, v);}
    
  
 
  /** @generated */
  final Feature casFeat_maltdephead;
  /** @generated */
  final int     casFeatCode_maltdephead;
  /** @generated */ 
  public int getMaltdephead(int addr) {
        if (featOkTst && casFeat_maltdephead == null)
      jcas.throwFeatMissing("maltdephead", "werti.uima.types.annot.Token");
    return ll_cas.ll_getIntValue(addr, casFeatCode_maltdephead);
  }
  /** @generated */    
  public void setMaltdephead(int addr, int v) {
        if (featOkTst && casFeat_maltdephead == null)
      jcas.throwFeatMissing("maltdephead", "werti.uima.types.annot.Token");
    ll_cas.ll_setIntValue(addr, casFeatCode_maltdephead, v);}
    
  
 
  /** @generated */
  final Feature casFeat_maltdeprel;
  /** @generated */
  final int     casFeatCode_maltdeprel;
  /** @generated */ 
  public String getMaltdeprel(int addr) {
        if (featOkTst && casFeat_maltdeprel == null)
      jcas.throwFeatMissing("maltdeprel", "werti.uima.types.annot.Token");
    return ll_cas.ll_getStringValue(addr, casFeatCode_maltdeprel);
  }
  /** @generated */    
  public void setMaltdeprel(int addr, String v) {
        if (featOkTst && casFeat_maltdeprel == null)
      jcas.throwFeatMissing("maltdeprel", "werti.uima.types.annot.Token");
    ll_cas.ll_setStringValue(addr, casFeatCode_maltdeprel, v);}
    
  



  /** initialize variables to correspond with Cas Type and Features
	* @generated */
  public Token_Type(JCas jcas, Type casType) {
    super(jcas, casType);
    casImpl.getFSClassRegistry().addGeneratorForType((TypeImpl)this.casType, getFSGenerator());

 
    casFeat_tag = jcas.getRequiredFeatureDE(casType, "tag", "uima.cas.String", featOkTst);
    casFeatCode_tag  = (null == casFeat_tag) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_tag).getCode();

 
    casFeat_detailedtag = jcas.getRequiredFeatureDE(casType, "detailedtag", "uima.cas.String", featOkTst);
    casFeatCode_detailedtag  = (null == casFeat_detailedtag) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_detailedtag).getCode();

 
    casFeat_lemma = jcas.getRequiredFeatureDE(casType, "lemma", "uima.cas.String", featOkTst);
    casFeatCode_lemma  = (null == casFeat_lemma) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_lemma).getCode();

 
    casFeat_gerund = jcas.getRequiredFeatureDE(casType, "gerund", "uima.cas.String", featOkTst);
    casFeatCode_gerund  = (null == casFeat_gerund) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_gerund).getCode();

 
    casFeat_chunk = jcas.getRequiredFeatureDE(casType, "chunk", "uima.cas.String", featOkTst);
    casFeatCode_chunk  = (null == casFeat_chunk) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_chunk).getCode();

 
    casFeat_mltag = jcas.getRequiredFeatureDE(casType, "mltag", "uima.cas.String", featOkTst);
    casFeatCode_mltag  = (null == casFeat_mltag) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_mltag).getCode();

 
    casFeat_depid = jcas.getRequiredFeatureDE(casType, "depid", "uima.cas.Integer", featOkTst);
    casFeatCode_depid  = (null == casFeat_depid) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_depid).getCode();

 
    casFeat_dephead = jcas.getRequiredFeatureDE(casType, "dephead", "uima.cas.Integer", featOkTst);
    casFeatCode_dephead  = (null == casFeat_dephead) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_dephead).getCode();

 
    casFeat_deprel = jcas.getRequiredFeatureDE(casType, "deprel", "uima.cas.String", featOkTst);
    casFeatCode_deprel  = (null == casFeat_deprel) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_deprel).getCode();

 
    casFeat_maltdepid = jcas.getRequiredFeatureDE(casType, "maltdepid", "uima.cas.Integer", featOkTst);
    casFeatCode_maltdepid  = (null == casFeat_maltdepid) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_maltdepid).getCode();

 
    casFeat_maltdephead = jcas.getRequiredFeatureDE(casType, "maltdephead", "uima.cas.Integer", featOkTst);
    casFeatCode_maltdephead  = (null == casFeat_maltdephead) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_maltdephead).getCode();

 
    casFeat_maltdeprel = jcas.getRequiredFeatureDE(casType, "maltdeprel", "uima.cas.String", featOkTst);
    casFeatCode_maltdeprel  = (null == casFeat_maltdeprel) ? JCas.INVALID_FEATURE_CODE : ((FeatureImpl)casFeat_maltdeprel).getCode();

  }
}



    