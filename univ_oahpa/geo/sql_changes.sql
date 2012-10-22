BEGIN;
ALTER TABLE `univ_drill_log` ADD COLUMN `user_ip` char(15);
ALTER TABLE `univ_drill_log` ADD COLUMN `user_country` varchar(8) ;
ALTER TABLE `univ_drill_log` ADD COLUMN `user_city` varchar(30) ;
COMMIT;
