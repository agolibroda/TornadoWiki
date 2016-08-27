SET FOREIGN_KEY_CHECKS = 0; 


-- Дамп структуры для таблица wiki.annotations
DROP TABLE IF EXISTS annotations;
CREATE TABLE IF NOT EXISTS annotations (
  article_id int(10) unsigned NOT NULL,
  annotation_text tinytext NOT NULL,
  annotation_sha_hash varchar(66) NOT NULL,
  PRIMARY KEY (annotation_sha_hash),
  KEY annotation_article_id (article_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы wiki.annotations: ~5 rows (приблизительно)
/*!40000 ALTER TABLE annotations DISABLE KEYS */;
INSERT INTO annotations (article_id, annotation_text, annotation_sha_hash) VALUES
	(2, '0KHQu9GD0LbQtdCx0L3Ri9C1INGB0YLQsNGC0YzQuA==', '3312f2f071e0c4c50c9165159db773750761d6a9bbf73bacd2270d6d868d1dd0'),
	(4, '0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90LDRjyDRgdGC0LDRgtGM0Y8=', '5bef2d09b4f5f2110373870af4c9c7e0ddc135fe029087508538fc950d5b97da'),
	(1, '0KHQv9C40YHQvtC6INCa0LDRgtC10LPQvtGA0LjQuSDRgdGC0LDRgtC10Lk=', '8402d4bffd9334332c82c79ac1c226eba896aec279027172a4e1c0c29231766f'),
	(3, '0KjQsNCx0LvQvtC90Ys=', '8c0f4c6dfae1b203f4f6f4ce4476c2dbf2077d91a6ab12ad290bb66328e8081c'),
	(6, '0J7RgdC90L7QstC90L7QuSDRiNCw0LHQu9C+0L0g0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90L7QuSDRgtGA0LDQvdC40YbRiw==', 'c9761801d393a57c1bf154f9ad58d01c5c6abf9b06272bfc6a7cf70d3e4532b7'),
	(5, '0JPQu9Cw0LLQvdCw0Y8g0YHRgtCw0YLRjNGPINGB0LDQudGC0LA=', 'cd0a31e15ed0f494158e78d79a554ee926a2583e56868a9cf3b7d53cbc207bff');
/*!40000 ALTER TABLE annotations ENABLE KEYS */;


-- Дамп структуры для таблица wiki.articles
DROP TABLE IF EXISTS articles;
CREATE TABLE IF NOT EXISTS articles (
  article_id int(10) unsigned NOT NULL AUTO_INCREMENT,
  article_title tinytext NOT NULL,
  article_annotation text,
  article_html mediumtext NOT NULL,
  category_article_id int(10) unsigned NOT NULL,
  template int(10) unsigned DEFAULT NULL,
  permissions enum('pbl','grp','sol') NOT NULL DEFAULT 'pbl',
  PRIMARY KEY (article_id),
  UNIQUE KEY article_title (article_title(100)),
  KEY article_id_idx (article_id),
  KEY type (category_article_id),
  KEY template (template),
  KEY permissions (permissions),
  KEY category_article_id (category_article_id)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы wiki.articles: ~6 rows (приблизительно)
/*!40000 ALTER TABLE articles DISABLE KEYS */;
INSERT INTO articles (article_id, article_title, article_annotation, article_html, category_article_id, template, permissions) VALUES
	(1, '0KHQv9C40YHQvtC6INCa0LDRgtC10LPQvtGA0LjQuSDRgdGC0LDRgtC10Lk=', '0KHQv9C40YHQvtC6INCa0LDRgtC10LPQvtGA0LjQuSDRgdGC0LDRgtC10Lk=', 'PHA+0KHQv9C40YHQvtC6INCa0LDRgtC10LPQvtGA0LjQuSDRgdGC0LDRgtC10Lk8L3A+', 0, NULL, 'pbl'),
	(2, '0KHQu9GD0LbQtdCx0L3Ri9C1INGB0YLQsNGC0YzQuA==', '0KHQu9GD0LbQtdCx0L3Ri9C1INGB0YLQsNGC0YzQuA==', 'PHA+0KHQu9GD0LbQtdCx0L3Ri9C1INGB0YLQsNGC0YzQuDwvcD4=', 1, NULL, 'pbl'),
	(3, '0KjQsNCx0LvQvtC90Ys=', '0KjQsNCx0LvQvtC90Ys=', 'PHA+0KjQsNCx0LvQvtC90Ys8L3A+', 1, NULL, 'pbl'),
	(4, '0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90LDRjyDRgdGC0LDRgtGM0Y8=', '0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90LDRjyDRgdGC0LDRgtGM0Y8=', 'PHA+0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90LDRjyDRgdGC0LDRgtGM0Y88L3A+', 1, NULL, 'pbl'),
	(5, '0JPQu9Cw0LLQvdCw0Y8g0YHRgtCw0YLRjNGPINGB0LDQudGC0LA=', '0JPQu9Cw0LLQvdCw0Y8g0YHRgtCw0YLRjNGPINGB0LDQudGC0LA=', 'PHA+0JPQu9Cw0LLQvdCw0Y8g0YHRgtCw0YLRjNGPINGB0LDQudGC0LA8L3A+', 4, NULL, 'pbl'),
	(6, '0J7RgdC90L7QstC90L7QuSDRiNCw0LHQu9C+0L0g0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90L7QuSDRgtGA0LDQvdC40YbRiw==', '0J7RgdC90L7QstC90L7QuSDRiNCw0LHQu9C+0L0g0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90L7QuSDRgtGA0LDQvdC40YbRiw==', 'PCFET0NUWVBFIGh0bWw+DQo8aHRtbD4NCjxoZWFkPg0KPG1ldGEgY2hhcnNldD0iVVRGLTgiPg0KPHRpdGxlPlRvcm5hZG8gV2lraSBBZG1pbiBsYXllcjwvdGl0bGU+DQo8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Ii9zdGF0aWMvd2lraS5jc3MiIHR5cGU9InRleHQvY3NzIj4NCjxsaW5rIHJlbD0iYWx0ZXJuYXRlIiBocmVmPSIvZmVlZCIgdHlwZT0iYXBwbGljYXRpb24vYXRvbSt4bWwiIA0KdGl0bGU9IltbdGl0bGVdXSI+DQoNCjwvaGVhZD4NCjxib2R5Pg0KPGRpdiBpZD0iYm9keSI+DQo8ZGl2IGlkPSJoZWFkZXIiPg0KPGRpdiBzdHlsZT0iZmxvYXQ6cmlnaHQiPg0KDQo8YSBocmVmPSIvYXV0aC9sb2dpbiI+U2lnbiBpbjwvYT4gdG8gY29tcG9zZS9lZGl0DQoNCjwvZGl2Pg0KPGgxPjxhIGhyZWY9Ii8iPtCd0LAg0JPQu9Cw0LLQvdGD0Y48L2E+PC9oMT4NCjwvZGl2Pg0KPCEtLSB1c2VyIElTOiBOb25lIC0tPg0KPGRpdiBpZD0iY29udGVudCI+DQoNCjwhLS0gbW9kdWxlcy9hcnRpY2xlLmh0bWwgLS0+DQo8ZGl2IGNsYXNzPSJhcnRpY2xlIj4NCjxoMT48YSBocmVmPSJbW11dIj5bW2FydGljbGUuYXJ0aWNsZV90aXRsZV1dPC9hPjwvaDE+DQo8ZGl2IGNsYXNzPSJib2R5Ij5bW2FydGljbGUuYXJ0aWNsZV9hbm5vdGF0aW9ual1dPC9kaXY+DQo8ZGl2IGNsYXNzPSJib2R5Ij4NCltbYXJ0aWNsZS5hcnRpY2xlX2h0bWxdXQ0KPGJyPg0KPCEtLSBtb2R1bGVzL2ZpbGVzX2xpc3QuaHRtbCAtLT4NCltbZmlsZUxpc3RdXQ0KPCEtLSAvIG1vZHVsZXMvZmlsZXNfbGlzdC5odG1sIC0tPg0KPC9kaXY+DQo8ZGl2IGNsYXNzPSJhZG1pbiI+DQpbPGEgaHJlZj0iW1thcnRpY2xlLmFydGljbGVfaWRdXSI+RWRpdCB0aGlzIHdpa2k8L2E+XQ0KWzxhIGhyZWY9IltbYXJ0aWNsZS5hcnRpY2xlX2lkXV0iPlZpZXcgYWxsIHJldmlzaW9uczwvYT5dDQo8L2Rpdj4NCjwvZGl2Pg0KDQo8L2Rpdj4NCjwvZGl2Pg0KDQo8L2JvZHk+DQo8L2h0bWw+', 0, NULL, 'pbl');
/*!40000 ALTER TABLE articles ENABLE KEYS */;


-- Дамп структуры для таблица wiki.files
DROP TABLE IF EXISTS files;
CREATE TABLE IF NOT EXISTS files (
  file_id int(10) unsigned NOT NULL AUTO_INCREMENT,
  user_id int(10) unsigned NOT NULL,
  file_create_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  file_inside_name varchar(66) NOT NULL,
  file_extension varchar(20) NOT NULL,
  file_name varchar(254) NOT NULL,
  PRIMARY KEY (file_id),
  UNIQUE KEY file_inside_name (file_inside_name),
  KEY file_create_date (file_create_date),
  KEY file_extension (file_extension),
  KEY file_name (file_name),
  KEY user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы wiki.files: ~0 rows (приблизительно)
/*!40000 ALTER TABLE files DISABLE KEYS */;
/*!40000 ALTER TABLE files ENABLE KEYS */;


-- Дамп структуры для таблица wiki.files_kroses
DROP TABLE IF EXISTS files_kroses;
CREATE TABLE IF NOT EXISTS files_kroses (
  file_id int(10) unsigned NOT NULL,
  article_id int(10) unsigned NOT NULL,
  file_kros_create_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  file_kros_flag enum('A','M') NOT NULL,
  PRIMARY KEY (file_id,article_id),
  KEY file_id (file_id),
  KEY article_id (article_id),
  KEY file_kros_create_date (file_kros_create_date),
  KEY file_kros_flag (file_kros_flag)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы wiki.files_kroses: ~0 rows (приблизительно)
/*!40000 ALTER TABLE files_kroses DISABLE KEYS */;
/*!40000 ALTER TABLE files_kroses ENABLE KEYS */;


-- Дамп структуры для таблица wiki.revisions
DROP TABLE IF EXISTS revisions;
CREATE TABLE IF NOT EXISTS revisions (
  revision_id int(10) unsigned NOT NULL AUTO_INCREMENT,
  article_id int(10) unsigned NOT NULL,
  user_id int(10) unsigned NOT NULL,
  revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revision_actual_flag enum('A','N') NOT NULL,
  title_sha_hash varchar(66) NOT NULL,
  annotation_sha_hash varchar(66) NOT NULL,
  text_sha_hash varchar(66) NOT NULL,
  PRIMARY KEY (revision_id),
  KEY article_id_rev (article_id),
  KEY revision_date (revision_date),
  KEY title_sha_hash (title_sha_hash),
  KEY annotation_sha_hash (annotation_sha_hash),
  KEY text_sha_hash (text_sha_hash),
  KEY user_id (user_id),
  KEY revision_actual_flag (revision_actual_flag)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы wiki.revisions: ~5 rows (приблизительно)
/*!40000 ALTER TABLE revisions DISABLE KEYS */;
INSERT INTO revisions (revision_id, article_id, user_id, revision_date, revision_actual_flag, title_sha_hash, annotation_sha_hash, text_sha_hash) VALUES
	(1, 1, 1, '2016-08-11 09:33:43', 'A', '136e050397813d0297c61a5ab8ecb24928896a4b282f0a4be52de7bf19e2907d', '8402d4bffd9334332c82c79ac1c226eba896aec279027172a4e1c0c29231766f', 'c41af4fe916911c79460ec66c912a82868bdaadca6fbeb5329953f8e3b074b15'),
	(2, 2, 1, '2016-08-11 09:34:11', 'A', '9a28c9f82da29ef3ecc8052d88363a3b3bc0ae6e4c250743b17a27a4398c8a1a', '3312f2f071e0c4c50c9165159db773750761d6a9bbf73bacd2270d6d868d1dd0', 'ff0917f405ec86faeff00de5eed8e26b9fea3680a2cbf5ae99aafa49bd324fb8'),
	(3, 3, 1, '2016-08-11 09:34:31', 'A', '99d49ee10b9e1309e286af411756e97d90d11dc9763be58299fa89ae8c3fb6f2', '8c0f4c6dfae1b203f4f6f4ce4476c2dbf2077d91a6ab12ad290bb66328e8081c', 'ee5c6e6d845e957e61f43fcc4919ad78452cd2fa770d61897042aa2e1c69766c'),
	(4, 4, 1, '2016-08-11 09:34:53', 'A', '0e27a9d729935babb7f9489e627ea7fb83599136684370b3ff327269ff2d1b5f', '5bef2d09b4f5f2110373870af4c9c7e0ddc135fe029087508538fc950d5b97da', 'a2bdf727661b4064802c9c1a4858d7fb07b6db7ef196e77c7367ac054ff99035'),
	(5, 5, 1, '2016-08-11 09:36:25', 'A', '49f68ae49b1599586d02a26ffd33f3d9bd26bbf8f2b624efef7abd21151c7ded', 'cd0a31e15ed0f494158e78d79a554ee926a2583e56868a9cf3b7d53cbc207bff', '9ab19d7ebab9c72a557be2fb02631f8eac77729515b23b9c47f9daa43a71cc50'),
	(7, 6, 1, '2016-08-11 09:38:03', 'A', '948dd6cf954e1e903c92f3aff231d0294a3436d6668abea5ec4d260d0cf7f2e9', 'c9761801d393a57c1bf154f9ad58d01c5c6abf9b06272bfc6a7cf70d3e4532b7', 'd7fffbc3e9889af9c2d0c34396aa417fd385c5ad516773426a14a4201e21b5dd');
/*!40000 ALTER TABLE revisions ENABLE KEYS */;


-- Дамп структуры для таблица wiki.texts
DROP TABLE IF EXISTS texts;
CREATE TABLE IF NOT EXISTS texts (
  article_id int(10) unsigned NOT NULL,
  text_sha_hash varchar(66) NOT NULL,
  text_html mediumtext NOT NULL,
  PRIMARY KEY (text_sha_hash),
  KEY article_article_id_id (article_id),
  KEY article_text_sha_hash_id (text_sha_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы wiki.texts: ~5 rows (приблизительно)
/*!40000 ALTER TABLE texts DISABLE KEYS */;
INSERT INTO texts (article_id, text_sha_hash, text_html) VALUES
	(5, '9ab19d7ebab9c72a557be2fb02631f8eac77729515b23b9c47f9daa43a71cc50', 'eJyzKbC7MPnC7gsbLmy6sPfChov9ChcbLzYBGU0Xe8AcoMxOkICNfoEdAJZhHAQ='),
	(4, 'a2bdf727661b4064802c9c1a4858d7fb07b6db7ef196e77c7367ac054ff99035', 'eJyzKbC7MOPC3ostF/ZdbLiw58KGi20XdlzYd2EvEG642K9wsfFiE5DRdLHnYr+NfoEdAA8eHvU='),
	(1, 'c41af4fe916911c79460ec66c912a82868bdaadca6fbeb5329953f8e3b074b15', 'eJyzKbC7sPDC/gs7LjZe2Hdhl8KFWRc2XGy6sPXC5gv7LjZc2HFhp8LFRqAARHCnjX6BHQBpwyDx'),
	(6, 'd7fffbc3e9889af9c2d0c34396aa417fd385c5ad516773426a14a4201e21b5dd', 'eJyNU8Fq20AQvRv8D5O9FmXJrQRLUNIUCqUtxG0pQoSNNLa2We2a3XESn3vvpef+Q8i19B+UP+qOLLmqHUovGu3svKc3b0azo5fvzuaf359DTY3JppPZLqKqODZICspa+YCUig/zV8lzwXnSZDCbO29V5eCTvtbwomq0BaM26Gdyex8LjbbX4NGkItDGYKgRSUDtcZEKGUiRLuVthB+XIQigzQpTQXhHks9/EyhDGL9HuMMvEKsBpFYro8vI56xU5Jpnd40RMJ10SlKR591LUTBppJVDh1eu2nCs9A3oKhV8FuMEF6Lfpbo2UrEwTtGp18uaekY1qFJrqqVxS21FdqGXFrSdSZUBOShds3IBJVaatjIiZef3SfaHQGTtj/Ye2u/tz/a+fWh/PX59/MYUUfVJNkIdJQmsA3p4fXEKb51FSJKx9NJZQjsI5OrGVes4Bal8NN7gMc97BCqNCiF6ub0V+8rynP3L8wHdx8ve2rHEEdvW0UOUstZRN7AvjO17OgBOJ4dQll0UPD2f7XW20PF5aXSgUXN5zuk3MdmhuF7+G/GUHsUb3gkaObIvTVfs0XkcMFCtA/ByszHF/8A+arwFZUxc+BsdojOhh+7k9PHpzLDLsvuNfwNBWj+4'),
	(3, 'ee5c6e6d845e957e61f43fcc4919ad78452cd2fa770d61897042aa2e1c69766c', 'eJyzKbC7sOLChgsbL+y+sO/C3ovdNvoFdgCOSgx/'),
	(2, 'ff0917f405ec86faeff00de5eed8e26b9fea3680a2cbf5ae99aafa49bd324fb8', 'eJwBJgDZ/zxwPtCh0LvRg9C20LXQsdC90YvQtSDRgdGC0LDRgtGM0Lg8L3A+3r0Xyw==');
/*!40000 ALTER TABLE texts ENABLE KEYS */;


-- Дамп структуры для таблица wiki.titles
DROP TABLE IF EXISTS titles;
CREATE TABLE IF NOT EXISTS titles (
  article_id int(10) unsigned NOT NULL,
  title_text tinytext NOT NULL,
  title_sha_hash varchar(66) NOT NULL,
  PRIMARY KEY (title_sha_hash),
  KEY title_article_id (article_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Дамп данных таблицы wiki.titles: ~5 rows (приблизительно)
/*!40000 ALTER TABLE titles DISABLE KEYS */;
INSERT INTO titles (article_id, title_text, title_sha_hash) VALUES
	(4, '0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90LDRjyDRgdGC0LDRgtGM0Y8=', '0e27a9d729935babb7f9489e627ea7fb83599136684370b3ff327269ff2d1b5f'),
	(1, '0KHQv9C40YHQvtC6INCa0LDRgtC10LPQvtGA0LjQuSDRgdGC0LDRgtC10Lk=', '136e050397813d0297c61a5ab8ecb24928896a4b282f0a4be52de7bf19e2907d'),
	(5, '0JPQu9Cw0LLQvdCw0Y8g0YHRgtCw0YLRjNGPINGB0LDQudGC0LA=', '49f68ae49b1599586d02a26ffd33f3d9bd26bbf8f2b624efef7abd21151c7ded'),
	(6, '0J7RgdC90L7QstC90L7QuSDRiNCw0LHQu9C+0L0g0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90L7QuSDRgtGA0LDQvdC40YbRiw==', '948dd6cf954e1e903c92f3aff231d0294a3436d6668abea5ec4d260d0cf7f2e9'),
	(3, '0KjQsNCx0LvQvtC90Ys=', '99d49ee10b9e1309e286af411756e97d90d11dc9763be58299fa89ae8c3fb6f2'),
	(2, '0KHQu9GD0LbQtdCx0L3Ri9C1INGB0YLQsNGC0YzQuA==', '9a28c9f82da29ef3ecc8052d88363a3b3bc0ae6e4c250743b17a27a4398c8a1a');
/*!40000 ALTER TABLE titles ENABLE KEYS */;


-- Дамп структуры для таблица wiki.users
DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
  user_id int(10) unsigned NOT NULL AUTO_INCREMENT,
  user_create timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  user_login varchar(50) NOT NULL,
  user_name varchar(254) DEFAULT NULL,
  user_pass varchar(70) DEFAULT NULL,
  user_role enum('admin','volunteer') NOT NULL DEFAULT 'volunteer',
  user_phon varchar(50) DEFAULT NULL,
  user_email varchar(254) DEFAULT NULL,
  user_external varchar(50) DEFAULT NULL,
  PRIMARY KEY (user_id),
  UNIQUE KEY user_login (user_login),
  KEY user_name (user_name),
  KEY user_pass (user_pass),
  KEY user_phon (user_phon),
  KEY user_email (user_email)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- Дамп данных таблицы wiki.users: ~1 rows (приблизительно)
/*!40000 ALTER TABLE users DISABLE KEYS */;
INSERT INTO users (user_id, user_create, user_login, user_name, user_pass, user_role, user_phon, user_email, user_external) VALUES
	(1, '2015-12-25 12:53:08', 'login', 'MyName And SurName ewrwerwerw', '$2b$12$.b9454ab5a22859b68bb4uvIvIvpREbnd9t2DJ7rqm1bwB/PrsH0.', 'admin', '1234-65432-4444', 'mail_0001@mail.com', '');


SET FOREIGN_KEY_CHECKS = 1;
	