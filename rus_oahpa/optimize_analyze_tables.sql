SELECT `rusdrill_word`.`id`, `rusdrill_word`.`lemma` FROM `rusdrill_word` INNER JOIN `rusdrill_word_semtype` T4 ON (`rusdrill_word`.`id` = T4.`word_id`) INNER JOIN `rusdrill_semtype` T5 ON (T4.`semtype_id` = T5.`id`) INNER JOIN `rusdrill_wordtranslation` ON (`rusdrill_word`.`id` = `rusdrill_wordtranslation`.`word_id`) WHERE (NOT ((`rusdrill_word`.`id` IN (SELECT U1.`word_id` FROM `rusdrill_word_semtype` U1 INNER JOIN `rusdrill_semtype` U2 ON (U1.`semtype_id` = U2.`id`) WHERE U2.`semtype` IN ('exclude_rusnob', 'mPERSNAME', 'PLACES')) AND `rusdrill_word`.`id` IS NOT NULL)) AND T5.`semtype` IN ('HUMAN') AND `rusdrill_wordtranslation`.`language` = 'rus'  AND `rusdrill_word`.`language` = 'swe' ) ORDER BY RAND() LIMIT 10 ;

ANALYZE TABLE `rusdrill_word` ; 
ANALYZE TABLE `rusdrill_word_source` ; 
ANALYZE TABLE `rusdrill_word_semtype` ; 
ANALYZE TABLE `rusdrill_semtype` ; 
ANALYZE TABLE `rusdrill_wordtranslation` ; 
ANALYZE TABLE `rusdrill_word` ; 
ANALYZE TABLE `rusdrill_word_dialects` ; 
ANALYZE TABLE `rusdrill_word_semtype` ; 
ANALYZE TABLE `rusdrill_word_source` ; 
ANALYZE TABLE `rusdrill_wordqelement` ; 
ANALYZE TABLE `rusdrill_wordtranslation` ; 
ANALYZE TABLE `rusdrill_wordtranslation_semtype` ; 
ANALYZE TABLE `rusdrill_wordtranslation_source` ; 

OPTIMIZE TABLE `rusdrill_word` ; 
OPTIMIZE TABLE `rusdrill_word_source` ; 
OPTIMIZE TABLE `rusdrill_word_semtype` ; 
OPTIMIZE TABLE `rusdrill_semtype` ; 
OPTIMIZE TABLE `rusdrill_wordtranslation` ; 
OPTIMIZE TABLE `rusdrill_word` ; 
OPTIMIZE TABLE `rusdrill_word_dialects` ; 
OPTIMIZE TABLE `rusdrill_word_semtype` ; 
OPTIMIZE TABLE `rusdrill_word_source` ; 
OPTIMIZE TABLE `rusdrill_wordqelement` ; 
OPTIMIZE TABLE `rusdrill_wordtranslation` ; 
OPTIMIZE TABLE `rusdrill_wordtranslation_semtype` ; 
OPTIMIZE TABLE `rusdrill_wordtranslation_source` ; 

SELECT `rusdrill_word`.`id`, `rusdrill_word`.`lemma` FROM `rusdrill_word` INNER JOIN `rusdrill_word_semtype` T4 ON (`rusdrill_word`.`id` = T4.`word_id`) INNER JOIN `rusdrill_semtype` T5 ON (T4.`semtype_id` = T5.`id`) INNER JOIN `rusdrill_wordtranslation` ON (`rusdrill_word`.`id` = `rusdrill_wordtranslation`.`word_id`) WHERE (NOT ((`rusdrill_word`.`id` IN (SELECT U1.`word_id` FROM `rusdrill_word_semtype` U1 INNER JOIN `rusdrill_semtype` U2 ON (U1.`semtype_id` = U2.`id`) WHERE U2.`semtype` IN ('exclude_rusnob', 'mPERSNAME', 'PLACES')) AND `rusdrill_word`.`id` IS NOT NULL)) AND T5.`semtype` IN ('HUMAN') AND `rusdrill_wordtranslation`.`language` = 'rus'  AND `rusdrill_word`.`language` = 'swe' ) ORDER BY RAND() LIMIT 10 ;
