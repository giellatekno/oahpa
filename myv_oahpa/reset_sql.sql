BEGIN;DROP TABLE `smadrill_grammarlinks`;
DROP TABLE `smadrill_wordqelement`;
ALTER TABLE `smadrill_qelement` DROP FOREIGN KEY `copy_id_refs_id_2aa06805`;
ALTER TABLE `smadrill_qelement` DROP FOREIGN KEY `agreement_id_refs_id_2aa06805`;
ALTER TABLE `smadrill_qelement_tags` DROP FOREIGN KEY `qelement_id_refs_id_1579cde`;
DROP TABLE `smadrill_qelement`;
DROP TABLE `smadrill_qelement_tags`;
ALTER TABLE `smadrill_question` DROP FOREIGN KEY `question_id_refs_id_61bd3037`;
ALTER TABLE `smadrill_question_source` DROP FOREIGN KEY `question_id_refs_id_38bcdaac`;
DROP TABLE `smadrill_question`;
DROP TABLE `smadrill_question_source`;
ALTER TABLE `smadrill_feedback_messages` DROP FOREIGN KEY `feedback_id_refs_id_45449755`;
ALTER TABLE `smadrill_feedback_dialects` DROP FOREIGN KEY `feedback_id_refs_id_2b920654`;
DROP TABLE `smadrill_feedback`;
DROP TABLE `smadrill_feedback_messages`;
DROP TABLE `smadrill_feedback_dialects`;
DROP TABLE `smadrill_feedbacktext`;
DROP TABLE `smadrill_feedbackmsg`;
ALTER TABLE `smadrill_form_dialects` DROP FOREIGN KEY `form_id_refs_id_6887c0a4`;
DROP TABLE `smadrill_form`;
DROP TABLE `smadrill_form_dialects`;
DROP TABLE `smadrill_tag`;
DROP TABLE `smadrill_tagname`;
DROP TABLE `smadrill_tagset`;
ALTER TABLE `smadrill_wordtranslation_semtype` DROP FOREIGN KEY `wordtranslation_id_refs_id_3a702e73`;
ALTER TABLE `smadrill_wordtranslation_source` DROP FOREIGN KEY `wordtranslation_id_refs_id_6c992a7c`;
DROP TABLE `smadrill_wordtranslation`;
DROP TABLE `smadrill_wordtranslation_semtype`;
DROP TABLE `smadrill_wordtranslation_source`;
ALTER TABLE `smadrill_word_source` DROP FOREIGN KEY `word_id_refs_id_4f0f0d1c`;
ALTER TABLE `smadrill_word_semtype` DROP FOREIGN KEY `word_id_refs_id_7ce43e3b`;
ALTER TABLE `smadrill_word_dialects` DROP FOREIGN KEY `word_id_refs_id_49975bc`;
DROP TABLE `smadrill_word`;
DROP TABLE `smadrill_word_source`;
DROP TABLE `smadrill_word_semtype`;
DROP TABLE `smadrill_word_dialects`;
DROP TABLE `smadrill_morphphontag`;
DROP TABLE `smadrill_dialect`;
DROP TABLE `smadrill_source`;
DROP TABLE `smadrill_semtype`;
DROP TABLE `smadrill_comment`;
CREATE TABLE `smadrill_comment` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `lang` varchar(5) NOT NULL,
    `comment` varchar(100) NOT NULL,
    `level` varchar(5) NOT NULL
)
;
CREATE TABLE `smadrill_semtype` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `semtype` varchar(50) NOT NULL
)
;
CREATE TABLE `smadrill_source` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `type` varchar(20) NOT NULL,
    `name` varchar(20) NOT NULL
)
;
CREATE TABLE `smadrill_dialect` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `dialect` varchar(5) NOT NULL,
    `name` varchar(100) NOT NULL
)
;
CREATE TABLE `smadrill_morphphontag` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `stem` varchar(20) NOT NULL,
    `wordclass` varchar(20) NOT NULL,
    `diphthong` varchar(20) NOT NULL,
    `gradation` varchar(20) NOT NULL,
    `rime` varchar(20) NOT NULL,
    `soggi` varchar(20) NOT NULL,
    UNIQUE (`stem`, `wordclass`, `diphthong`, `gradation`, `rime`, `soggi`)
)
;
CREATE TABLE `smadrill_word_dialects` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `word_id` integer NOT NULL,
    `dialect_id` integer NOT NULL,
    UNIQUE (`word_id`, `dialect_id`)
)
;
ALTER TABLE `smadrill_word_dialects` ADD CONSTRAINT `dialect_id_refs_id_724dc1fd` FOREIGN KEY (`dialect_id`) REFERENCES `smadrill_dialect` (`id`);
CREATE TABLE `smadrill_word_semtype` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `word_id` integer NOT NULL,
    `semtype_id` integer NOT NULL,
    UNIQUE (`word_id`, `semtype_id`)
)
;
ALTER TABLE `smadrill_word_semtype` ADD CONSTRAINT `semtype_id_refs_id_2bcbb4d5` FOREIGN KEY (`semtype_id`) REFERENCES `smadrill_semtype` (`id`);
CREATE TABLE `smadrill_word_source` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `word_id` integer NOT NULL,
    `source_id` integer NOT NULL,
    UNIQUE (`word_id`, `source_id`)
)
;
ALTER TABLE `smadrill_word_source` ADD CONSTRAINT `source_id_refs_id_79291ccd` FOREIGN KEY (`source_id`) REFERENCES `smadrill_source` (`id`);
CREATE TABLE `smadrill_word` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `wordid` varchar(200) NOT NULL,
    `language` varchar(5) NOT NULL,
    `lemma` varchar(200) NOT NULL,
    `presentationform` varchar(5) NOT NULL,
    `pos` varchar(12) NOT NULL,
    `stem` varchar(20) NOT NULL,
    `wordclass` varchar(8) NOT NULL,
    `valency` varchar(10) NOT NULL,
    `hid` integer,
    `diphthong` varchar(5) NOT NULL,
    `gradation` varchar(20) NOT NULL,
    `rime` varchar(20) NOT NULL,
    `attrsuffix` varchar(20) NOT NULL,
    `soggi` varchar(10) NOT NULL,
    `compare` varchar(5) NOT NULL,
    `frequency` varchar(10) NOT NULL,
    `geography` varchar(10) NOT NULL,
    `tcomm` bool NOT NULL,
    `morphophon_id` integer
)
;
ALTER TABLE `smadrill_word` ADD CONSTRAINT `morphophon_id_refs_id_39dc266` FOREIGN KEY (`morphophon_id`) REFERENCES `smadrill_morphphontag` (`id`);
ALTER TABLE `smadrill_word_dialects` ADD CONSTRAINT `word_id_refs_id_49975bc` FOREIGN KEY (`word_id`) REFERENCES `smadrill_word` (`id`);
ALTER TABLE `smadrill_word_semtype` ADD CONSTRAINT `word_id_refs_id_7ce43e3b` FOREIGN KEY (`word_id`) REFERENCES `smadrill_word` (`id`);
ALTER TABLE `smadrill_word_source` ADD CONSTRAINT `word_id_refs_id_4f0f0d1c` FOREIGN KEY (`word_id`) REFERENCES `smadrill_word` (`id`);
CREATE TABLE `smadrill_wordtranslation_source` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `wordtranslation_id` integer NOT NULL,
    `source_id` integer NOT NULL,
    UNIQUE (`wordtranslation_id`, `source_id`)
)
;
ALTER TABLE `smadrill_wordtranslation_source` ADD CONSTRAINT `source_id_refs_id_6b20c371` FOREIGN KEY (`source_id`) REFERENCES `smadrill_source` (`id`);
CREATE TABLE `smadrill_wordtranslation_semtype` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `wordtranslation_id` integer NOT NULL,
    `semtype_id` integer NOT NULL,
    UNIQUE (`wordtranslation_id`, `semtype_id`)
)
;
ALTER TABLE `smadrill_wordtranslation_semtype` ADD CONSTRAINT `semtype_id_refs_id_31c6a309` FOREIGN KEY (`semtype_id`) REFERENCES `smadrill_semtype` (`id`);
CREATE TABLE `smadrill_wordtranslation` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `word_id` integer NOT NULL,
    `language` varchar(5) NOT NULL,
    `wordid` varchar(200) NOT NULL,
    `lemma` varchar(200) NOT NULL,
    `phrase` longtext NOT NULL,
    `explanation` longtext NOT NULL,
    `pos` varchar(12) NOT NULL,
    `frequency` varchar(10) NOT NULL,
    `geography` varchar(10) NOT NULL,
    `tcomm` bool NOT NULL,
    `tcomm_pref` bool NOT NULL
)
;
ALTER TABLE `smadrill_wordtranslation` ADD CONSTRAINT `word_id_refs_id_29d9cf69` FOREIGN KEY (`word_id`) REFERENCES `smadrill_word` (`id`);
ALTER TABLE `smadrill_wordtranslation_source` ADD CONSTRAINT `wordtranslation_id_refs_id_6c992a7c` FOREIGN KEY (`wordtranslation_id`) REFERENCES `smadrill_wordtranslation` (`id`);
ALTER TABLE `smadrill_wordtranslation_semtype` ADD CONSTRAINT `wordtranslation_id_refs_id_3a702e73` FOREIGN KEY (`wordtranslation_id`) REFERENCES `smadrill_wordtranslation` (`id`);
CREATE TABLE `smadrill_tagset` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `tagset` varchar(25) NOT NULL
)
;
CREATE TABLE `smadrill_tagname` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `tagname` varchar(25) NOT NULL,
    `tagset_id` integer NOT NULL
)
;
ALTER TABLE `smadrill_tagname` ADD CONSTRAINT `tagset_id_refs_id_5fdd5c81` FOREIGN KEY (`tagset_id`) REFERENCES `smadrill_tagset` (`id`);
CREATE TABLE `smadrill_tag` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `string` varchar(25) NOT NULL,
    `attributive` varchar(5) NOT NULL,
    `case` varchar(5) NOT NULL,
    `conneg` varchar(5) NOT NULL,
    `grade` varchar(10) NOT NULL,
    `infinite` varchar(10) NOT NULL,
    `mood` varchar(5) NOT NULL,
    `number` varchar(5) NOT NULL,
    `personnumber` varchar(8) NOT NULL,
    `polarity` varchar(5) NOT NULL,
    `pos` varchar(12) NOT NULL,
    `possessive` varchar(5) NOT NULL,
    `subclass` varchar(10) NOT NULL,
    `tense` varchar(5) NOT NULL
)
;
CREATE TABLE `smadrill_form_dialects` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `form_id` integer NOT NULL,
    `dialect_id` integer NOT NULL,
    UNIQUE (`form_id`, `dialect_id`)
)
;
ALTER TABLE `smadrill_form_dialects` ADD CONSTRAINT `dialect_id_refs_id_1dda6985` FOREIGN KEY (`dialect_id`) REFERENCES `smadrill_dialect` (`id`);
CREATE TABLE `smadrill_form` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `word_id` integer NOT NULL,
    `tag_id` integer NOT NULL,
    `fullform` varchar(200) NOT NULL
)
;
ALTER TABLE `smadrill_form` ADD CONSTRAINT `tag_id_refs_id_612b816c` FOREIGN KEY (`tag_id`) REFERENCES `smadrill_tag` (`id`);
ALTER TABLE `smadrill_form` ADD CONSTRAINT `word_id_refs_id_d7d3083` FOREIGN KEY (`word_id`) REFERENCES `smadrill_word` (`id`);
ALTER TABLE `smadrill_form_dialects` ADD CONSTRAINT `form_id_refs_id_6887c0a4` FOREIGN KEY (`form_id`) REFERENCES `smadrill_form` (`id`);
CREATE TABLE `smadrill_feedbackmsg` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `msgid` varchar(100) NOT NULL
)
;
CREATE TABLE `smadrill_feedbacktext` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `message` varchar(200) NOT NULL,
    `language` varchar(6) NOT NULL,
    `feedbackmsg_id` integer NOT NULL
)
;
ALTER TABLE `smadrill_feedbacktext` ADD CONSTRAINT `feedbackmsg_id_refs_id_66e3c12e` FOREIGN KEY (`feedbackmsg_id`) REFERENCES `smadrill_feedbackmsg` (`id`);
CREATE TABLE `smadrill_feedback_dialects` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `feedback_id` integer NOT NULL,
    `dialect_id` integer NOT NULL,
    UNIQUE (`feedback_id`, `dialect_id`)
)
;
ALTER TABLE `smadrill_feedback_dialects` ADD CONSTRAINT `dialect_id_refs_id_6c452c04` FOREIGN KEY (`dialect_id`) REFERENCES `smadrill_dialect` (`id`);
CREATE TABLE `smadrill_feedback_messages` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `feedback_id` integer NOT NULL,
    `feedbackmsg_id` integer NOT NULL,
    UNIQUE (`feedback_id`, `feedbackmsg_id`)
)
;
ALTER TABLE `smadrill_feedback_messages` ADD CONSTRAINT `feedbackmsg_id_refs_id_10eb6f9` FOREIGN KEY (`feedbackmsg_id`) REFERENCES `smadrill_feedbackmsg` (`id`);
CREATE TABLE `smadrill_feedback` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `attrsuffix` varchar(10),
    `soggi` varchar(10),
    `stem` varchar(20),
    `wordclass` varchar(20),
    `attributive` varchar(10),
    `case2` varchar(5),
    `grade` varchar(10),
    `mood` varchar(10),
    `number` varchar(5),
    `personnumber` varchar(5),
    `pos` varchar(12),
    `tense` varchar(5),
    UNIQUE (`pos`, `stem`, `soggi`, `wordclass`, `case2`, `number`, `personnumber`, `tense`, `mood`, `grade`, `attrsuffix`, `attributive`)
)
;
ALTER TABLE `smadrill_feedback_dialects` ADD CONSTRAINT `feedback_id_refs_id_2b920654` FOREIGN KEY (`feedback_id`) REFERENCES `smadrill_feedback` (`id`);
ALTER TABLE `smadrill_feedback_messages` ADD CONSTRAINT `feedback_id_refs_id_45449755` FOREIGN KEY (`feedback_id`) REFERENCES `smadrill_feedback` (`id`);
CREATE TABLE `smadrill_question_source` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `question_id` integer NOT NULL,
    `source_id` integer NOT NULL,
    UNIQUE (`question_id`, `source_id`)
)
;
ALTER TABLE `smadrill_question_source` ADD CONSTRAINT `source_id_refs_id_175510f` FOREIGN KEY (`source_id`) REFERENCES `smadrill_source` (`id`);
CREATE TABLE `smadrill_question` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `qid` varchar(200) NOT NULL,
    `level` integer NOT NULL,
    `task` varchar(20) NOT NULL,
    `string` varchar(200) NOT NULL,
    `qtype` varchar(20) NOT NULL,
    `qatype` varchar(20) NOT NULL,
    `question_id` integer,
    `gametype` varchar(5) NOT NULL
)
;
ALTER TABLE `smadrill_question_source` ADD CONSTRAINT `question_id_refs_id_38bcdaac` FOREIGN KEY (`question_id`) REFERENCES `smadrill_question` (`id`);
ALTER TABLE `smadrill_question` ADD CONSTRAINT `question_id_refs_id_61bd3037` FOREIGN KEY (`question_id`) REFERENCES `smadrill_question` (`id`);
CREATE TABLE `smadrill_qelement_tags` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `qelement_id` integer NOT NULL,
    `tag_id` integer NOT NULL,
    UNIQUE (`qelement_id`, `tag_id`)
)
;
ALTER TABLE `smadrill_qelement_tags` ADD CONSTRAINT `tag_id_refs_id_54fac042` FOREIGN KEY (`tag_id`) REFERENCES `smadrill_tag` (`id`);
CREATE TABLE `smadrill_qelement` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `question_id` integer,
    `syntax` varchar(50) NOT NULL,
    `identifier` varchar(20) NOT NULL,
    `gametype` varchar(5) NOT NULL,
    `agreement_id` integer,
    `semtype_id` integer,
    `game` varchar(20) NOT NULL,
    `copy_id` integer
)
;
ALTER TABLE `smadrill_qelement` ADD CONSTRAINT `semtype_id_refs_id_3f64c042` FOREIGN KEY (`semtype_id`) REFERENCES `smadrill_semtype` (`id`);
ALTER TABLE `smadrill_qelement` ADD CONSTRAINT `question_id_refs_id_3ca43430` FOREIGN KEY (`question_id`) REFERENCES `smadrill_question` (`id`);
ALTER TABLE `smadrill_qelement_tags` ADD CONSTRAINT `qelement_id_refs_id_1579cde` FOREIGN KEY (`qelement_id`) REFERENCES `smadrill_qelement` (`id`);
ALTER TABLE `smadrill_qelement` ADD CONSTRAINT `agreement_id_refs_id_2aa06805` FOREIGN KEY (`agreement_id`) REFERENCES `smadrill_qelement` (`id`);
ALTER TABLE `smadrill_qelement` ADD CONSTRAINT `copy_id_refs_id_2aa06805` FOREIGN KEY (`copy_id`) REFERENCES `smadrill_qelement` (`id`);
CREATE TABLE `smadrill_wordqelement` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `word_id` integer,
    `qelement_id` integer
)
;
ALTER TABLE `smadrill_wordqelement` ADD CONSTRAINT `qelement_id_refs_id_6fe439d7` FOREIGN KEY (`qelement_id`) REFERENCES `smadrill_qelement` (`id`);
ALTER TABLE `smadrill_wordqelement` ADD CONSTRAINT `word_id_refs_id_72c495e0` FOREIGN KEY (`word_id`) REFERENCES `smadrill_word` (`id`);
CREATE TABLE `smadrill_grammarlinks` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(200),
    `address` varchar(800),
    `language` varchar(5)
)
;
CREATE INDEX `smadrill_word_feffdf0` ON `smadrill_word` (`morphophon_id`);
CREATE INDEX `smadrill_wordtranslation_4b95d890` ON `smadrill_wordtranslation` (`word_id`);
CREATE INDEX `smadrill_tagname_5e81f83a` ON `smadrill_tagname` (`tagset_id`);
CREATE INDEX `smadrill_form_4b95d890` ON `smadrill_form` (`word_id`);
CREATE INDEX `smadrill_form_3747b463` ON `smadrill_form` (`tag_id`);
CREATE INDEX `smadrill_feedbacktext_7afbc345` ON `smadrill_feedbacktext` (`feedbackmsg_id`);
CREATE INDEX `smadrill_question_1f92e550` ON `smadrill_question` (`question_id`);
CREATE INDEX `smadrill_qelement_1f92e550` ON `smadrill_qelement` (`question_id`);
CREATE INDEX `smadrill_qelement_4784a0db` ON `smadrill_qelement` (`agreement_id`);
CREATE INDEX `smadrill_qelement_4bd6d0ae` ON `smadrill_qelement` (`semtype_id`);
CREATE INDEX `smadrill_qelement_7aeacbd` ON `smadrill_qelement` (`copy_id`);
CREATE INDEX `smadrill_wordqelement_4b95d890` ON `smadrill_wordqelement` (`word_id`);
CREATE INDEX `smadrill_wordqelement_d0cde3f` ON `smadrill_wordqelement` (`qelement_id`);COMMIT;
