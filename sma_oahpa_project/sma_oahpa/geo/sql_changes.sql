BEGIN;
ALTER TABLE `drill_log` ADD COLUMN `user_country` varchar(8) ;
COMMIT;
