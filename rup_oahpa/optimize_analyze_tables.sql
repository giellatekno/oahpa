SELECT `smadrill_word`.`id`, `smadrill_word`.`lemma` FROM `smadrill_word` INNER JOIN `smadrill_word_semtype` T4 ON (`smadrill_word`.`id` = T4.`word_id`) INNER JOIN `smadrill_semtype` T5 ON (T4.`semtype_id` = T5.`id`) INNER JOIN `smadrill_wordtranslation` ON (`smadrill_word`.`id` = `smadrill_wordtranslation`.`word_id`) WHERE (NOT ((`smadrill_word`.`id` IN (SELECT U1.`word_id` FROM `smadrill_word_semtype` U1 INNER JOIN `smadrill_semtype` U2 ON (U1.`semtype_id` = U2.`id`) WHERE U2.`semtype` IN ('exclude_smanob', 'mPERSNAME', 'PLACES')) AND `smadrill_word`.`id` IS NOT NULL)) AND T5.`semtype` IN ('HUMAN') AND `smadrill_wordtranslation`.`language` = 'sma'  AND `smadrill_word`.`language` = 'swe' ) ORDER BY RAND() LIMIT 10 ;

ANALYZE TABLE `smadrill_word` ; 
ANALYZE TABLE `smadrill_word_source` ; 
ANALYZE TABLE `smadrill_word_semtype` ; 
ANALYZE TABLE `smadrill_semtype` ; 
ANALYZE TABLE `smadrill_wordtranslation` ; 
ANALYZE TABLE `smadrill_word` ; 
ANALYZE TABLE `smadrill_word_dialects` ; 
ANALYZE TABLE `smadrill_word_semtype` ; 
ANALYZE TABLE `smadrill_word_source` ; 
ANALYZE TABLE `smadrill_wordqelement` ; 
ANALYZE TABLE `smadrill_wordtranslation` ; 
ANALYZE TABLE `smadrill_wordtranslation_semtype` ; 
ANALYZE TABLE `smadrill_wordtranslation_source` ; 

OPTIMIZE TABLE `smadrill_word` ; 
OPTIMIZE TABLE `smadrill_word_source` ; 
OPTIMIZE TABLE `smadrill_word_semtype` ; 
OPTIMIZE TABLE `smadrill_semtype` ; 
OPTIMIZE TABLE `smadrill_wordtranslation` ; 
OPTIMIZE TABLE `smadrill_word` ; 
OPTIMIZE TABLE `smadrill_word_dialects` ; 
OPTIMIZE TABLE `smadrill_word_semtype` ; 
OPTIMIZE TABLE `smadrill_word_source` ; 
OPTIMIZE TABLE `smadrill_wordqelement` ; 
OPTIMIZE TABLE `smadrill_wordtranslation` ; 
OPTIMIZE TABLE `smadrill_wordtranslation_semtype` ; 
OPTIMIZE TABLE `smadrill_wordtranslation_source` ; 

SELECT `smadrill_word`.`id`, `smadrill_word`.`lemma` FROM `smadrill_word` INNER JOIN `smadrill_word_semtype` T4 ON (`smadrill_word`.`id` = T4.`word_id`) INNER JOIN `smadrill_semtype` T5 ON (T4.`semtype_id` = T5.`id`) INNER JOIN `smadrill_wordtranslation` ON (`smadrill_word`.`id` = `smadrill_wordtranslation`.`word_id`) WHERE (NOT ((`smadrill_word`.`id` IN (SELECT U1.`word_id` FROM `smadrill_word_semtype` U1 INNER JOIN `smadrill_semtype` U2 ON (U1.`semtype_id` = U2.`id`) WHERE U2.`semtype` IN ('exclude_smanob', 'mPERSNAME', 'PLACES')) AND `smadrill_word`.`id` IS NOT NULL)) AND T5.`semtype` IN ('HUMAN') AND `smadrill_wordtranslation`.`language` = 'sma'  AND `smadrill_word`.`language` = 'swe' ) ORDER BY RAND() LIMIT 10 ;
