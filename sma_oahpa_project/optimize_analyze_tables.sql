SELECT `drill_word`.`id`, `drill_word`.`lemma` FROM `drill_word` INNER JOIN `drill_word_semtype` T4 ON (`drill_word`.`id` = T4.`word_id`) INNER JOIN `drill_semtype` T5 ON (T4.`semtype_id` = T5.`id`) INNER JOIN `drill_wordtranslation` ON (`drill_word`.`id` = `drill_wordtranslation`.`word_id`) WHERE (NOT ((`drill_word`.`id` IN (SELECT U1.`word_id` FROM `drill_word_semtype` U1 INNER JOIN `drill_semtype` U2 ON (U1.`semtype_id` = U2.`id`) WHERE U2.`semtype` IN ('exclude_smanob', 'mPERSNAME', 'PLACES')) AND `drill_word`.`id` IS NOT NULL)) AND T5.`semtype` IN ('HUMAN') AND `drill_wordtranslation`.`language` = 'sma'  AND `drill_word`.`language` = 'swe' ) ORDER BY RAND() LIMIT 10 ;

ANALYZE TABLE `drill_word` ;
ANALYZE TABLE `drill_word_source` ;
ANALYZE TABLE `drill_word_semtype` ;
ANALYZE TABLE `drill_semtype` ;
ANALYZE TABLE `drill_wordtranslation` ;
ANALYZE TABLE `drill_word` ;
ANALYZE TABLE `drill_word_dialects` ;
ANALYZE TABLE `drill_word_semtype` ;
ANALYZE TABLE `drill_word_source` ;
ANALYZE TABLE `drill_wordqelement` ;
ANALYZE TABLE `drill_wordtranslation` ;
ANALYZE TABLE `drill_wordtranslation_semtype` ;
ANALYZE TABLE `drill_wordtranslation_source` ;

OPTIMIZE TABLE `drill_word` ;
OPTIMIZE TABLE `drill_word_source` ;
OPTIMIZE TABLE `drill_word_semtype` ;
OPTIMIZE TABLE `drill_semtype` ;
OPTIMIZE TABLE `drill_wordtranslation` ;
OPTIMIZE TABLE `drill_word` ;
OPTIMIZE TABLE `drill_word_dialects` ;
OPTIMIZE TABLE `drill_word_semtype` ;
OPTIMIZE TABLE `drill_word_source` ;
OPTIMIZE TABLE `drill_wordqelement` ;
OPTIMIZE TABLE `drill_wordtranslation` ;
OPTIMIZE TABLE `drill_wordtranslation_semtype` ;
OPTIMIZE TABLE `drill_wordtranslation_source` ;

SELECT `drill_word`.`id`, `drill_word`.`lemma` FROM `drill_word` INNER JOIN `drill_word_semtype` T4 ON (`drill_word`.`id` = T4.`word_id`) INNER JOIN `drill_semtype` T5 ON (T4.`semtype_id` = T5.`id`) INNER JOIN `drill_wordtranslation` ON (`drill_word`.`id` = `drill_wordtranslation`.`word_id`) WHERE (NOT ((`drill_word`.`id` IN (SELECT U1.`word_id` FROM `drill_word_semtype` U1 INNER JOIN `drill_semtype` U2 ON (U1.`semtype_id` = U2.`id`) WHERE U2.`semtype` IN ('exclude_smanob', 'mPERSNAME', 'PLACES')) AND `drill_word`.`id` IS NOT NULL)) AND T5.`semtype` IN ('HUMAN') AND `drill_wordtranslation`.`language` = 'sma'  AND `drill_word`.`language` = 'swe' ) ORDER BY RAND() LIMIT 10 ;
