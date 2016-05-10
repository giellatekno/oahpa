BEGIN;

-- Alter tables for columns below
ALTER TABLE `hdn_drill_dialect` CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci ;
ALTER TABLE `hdn_drill_form` CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci ;
ALTER TABLE `hdn_drill_semtype` CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci ;
ALTER TABLE `hdn_drill_source` CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci ;
ALTER TABLE `hdn_drill_word` CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci ;
ALTER TABLE `hdn_drill_wordtranslation` CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci ;


-- Alter individual columns
ALTER TABLE `hdn_drill_dialect` MODIFY name
    varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL ;
ALTER TABLE `hdn_drill_form` MODIFY fullform
    varchar(200) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL ;
ALTER TABLE `hdn_drill_semtype` MODIFY semtype
    varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL ;
ALTER TABLE `hdn_drill_source` MODIFY name
    varchar(20) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL ;
ALTER TABLE `hdn_drill_word` MODIFY lemma
    varchar(200) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL ;
ALTER TABLE `hdn_drill_wordtranslation` MODIFY explanation
    longtext CHARACTER SET utf8 COLLATE utf8_bin NOT NULL ;
ALTER TABLE `hdn_drill_wordtranslation` MODIFY lemma
    varchar(200) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL ;
ALTER TABLE `hdn_drill_wordtranslation` MODIFY phrase
    longtext CHARACTER SET utf8 COLLATE utf8_bin NOT NULL ;

COMMIT;

