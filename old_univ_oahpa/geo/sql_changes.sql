BEGIN;
ALTER TABLE `univ_drill_log` ADD COLUMN `user_country` varchar(8) ;
COMMIT;
