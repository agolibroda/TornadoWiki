--
-- Database: `wiki`
--

SET FOREIGN_KEY_CHECKS = 0; 
-- --------------------------------------------------------
--
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
CREATE TABLE IF NOT EXISTS `articles` (
  `article_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `article_title` tinytext NOT NULL,
  `article_annotation` text,
  `article_html` mediumtext NOT NULL,
  `category_article_id` int(10) unsigned NOT NULL,
  `template` int(10) unsigned DEFAULT NULL,
  `permissions` enum('pbl','grp','sol') NOT NULL DEFAULT 'pbl',
  PRIMARY KEY (`article_id`),
  UNIQUE KEY `article_title` (`article_title`(100)),
  KEY `article_id_idx` (`article_id`),
  KEY `type` (`category_article_id`),
  KEY `template` (`template`),
  KEY `permissions` (`permissions`),
  KEY `category_article_id` (`category_article_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;


-- --------------------------------------------------------

--
-- Table structure for table `files`
--

DROP TABLE IF EXISTS `files`;
CREATE TABLE `files` (
	`file_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`user_id` INT(10) UNSIGNED NOT NULL,
	`file_create_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`file_inside_name` VARCHAR(66) NOT NULL,
	`file_extension` VARCHAR(20) NOT NULL,
	`file_name` VARCHAR(254) NOT NULL,
	PRIMARY KEY (`file_id`),
	UNIQUE INDEX `file_inside_name` (`file_inside_name`),
	INDEX `file_create_date` (`file_create_date`),
	INDEX `file_extension` (`file_extension`),
	INDEX `file_name` (`file_name`),
	INDEX `user_id` (`user_id`)
)
COLLATE='utf8_general_ci' ENGINE=InnoDB;

-- --------------------------------------------------------

--
-- Table structure for table `files_kroses`
--

DROP TABLE IF EXISTS `files_kroses`;
CREATE TABLE IF NOT EXISTS `files_kroses` (
  `file_id` int(10) unsigned NOT NULL,
  `article_id` int(10) unsigned NOT NULL,
  `file_kros_create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `file_kros_flag` enum('A','M') NOT NULL,
  PRIMARY KEY (`file_id`,`article_id`),
  KEY `file_id` (`file_id`),
  KEY `article_id` (`article_id`),
  KEY `file_kros_create_date` (`file_kros_create_date`),
  KEY `file_kros_flag` (`file_kros_flag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `revisions`
--

DROP TABLE IF EXISTS `revisions`;
CREATE TABLE IF NOT EXISTS `revisions` (
  `revision_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `article_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `revision_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `revision_actual_flag` enum('A','N') NOT NULL,
  `title_sha_hash` varchar(66) NOT NULL,
  `annotation_sha_hash` varchar(66) NOT NULL,
  `text_sha_hash` varchar(66) NOT NULL,
  PRIMARY KEY (`revision_id`),
  KEY `article_id_rev` (`article_id`),
  KEY `revision_date` (`revision_date`),
  KEY `title_sha_hash` (`title_sha_hash`),
  KEY `annotation_sha_hash` (`annotation_sha_hash`),
  KEY `text_sha_hash` (`text_sha_hash`),
  KEY `user_id` (`user_id`),
  KEY `revision_actual_flag` (`revision_actual_flag`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=11 ;


-- --------------------------------------------------------

--
-- Table structure for table `annotations`
--

DROP TABLE IF EXISTS `annotations`;
CREATE TABLE IF NOT EXISTS `annotations` (
  `article_id` int(10) unsigned NOT NULL,
  `annotation_text` tinytext NOT NULL,
  `annotation_sha_hash` varchar(66) NOT NULL,
  PRIMARY KEY (`annotation_sha_hash`),
  KEY `annotation_article_id` (`article_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Table structure for table `texts`
--

DROP TABLE IF EXISTS `texts`;
CREATE TABLE IF NOT EXISTS `texts` (
  `article_id` int(10) unsigned NOT NULL,
  `text_sha_hash` varchar(66) NOT NULL,
  `text_html` mediumtext NOT NULL,
  PRIMARY KEY (`text_sha_hash`),
  KEY `article_article_id_id` (`article_id`),
  KEY `article_text_sha_hash_id` (`text_sha_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `titles`
--

DROP TABLE IF EXISTS `titles`;
CREATE TABLE IF NOT EXISTS `titles` (
  `article_id` int(10) unsigned NOT NULL,
  `title_text` tinytext NOT NULL,
  `title_sha_hash` varchar(66) NOT NULL,
  PRIMARY KEY (`title_sha_hash`),
  KEY `title_article_id` (`article_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_create` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_login` varchar(50) NOT NULL,
  `user_name` varchar(254) DEFAULT NULL,
  `user_pass` varchar(70) DEFAULT NULL,
  `user_role` enum('admin','volunteer') NOT NULL DEFAULT 'volunteer',
  `user_phon` varchar(50) DEFAULT NULL,
  `user_email` varchar(254) DEFAULT NULL,
  `user_external` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_login` (`user_login`),
  KEY `user_name` (`user_name`),
  KEY `user_pass` (`user_pass`),
  KEY `user_phon` (`user_phon`),
  KEY `user_email` (`user_email`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `user_create`, `user_login`, `user_name`, `user_pass`, `user_role`, `user_phon`, `user_email`, `user_external`) VALUES
(1, '2015-12-25 12:53:08', 'login', 'MyName And SurName ewrwerwerw', '$2b$12$.b9454ab5a22859b68bb4uvIvIvpREbnd9t2DJ7rqm1bwB/PrsH0.', 'admin', '1234-65432-4444', 'mail_0001@mail.com', '');


  
  SET FOREIGN_KEY_CHECKS = 1; 