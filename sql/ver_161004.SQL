
DROP TYPE IF EXISTS revision_type CASCADE;
CREATE TYPE revision_type AS enum('A','N', 'D');


DROP TYPE IF EXISTS author_type;
CREATE TYPE author_type AS enum('admin','volunteer');

-- Дамп структуры для таблица wiki.authors
DROP SEQUENCE IF EXISTS authors_author_id_seq;
CREATE SEQUENCE IF NOT EXISTS authors_author_id_seq;


DROP TABLE IF EXISTS authors;
CREATE TABLE IF NOT EXISTS authors (
  author_id int unique not null DEFAULT nextval('authors_author_id_seq') primary key,
  author_create timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  author_login varchar(50) NOT NULL,
  author_name varchar(254) DEFAULT NULL,
  author_external varchar(50) DEFAULT NULL,
  author_pass varchar(70) DEFAULT NULL,
  author_phon varchar(50) DEFAULT NULL,
  author_email varchar(254) DEFAULT NULL,
  author_role author_type NOT NULL DEFAULT 'volunteer'
);

CREATE INDEX authors_author_name ON authors (author_name);
CREATE INDEX authors_author_pass ON authors (author_pass);
CREATE INDEX authors_author_phon ON authors (author_phon);
CREATE INDEX authors_author_email ON authors (author_email);



--SET FOREIGN_KEY_CHECKS = 0; 

DROP TYPE IF EXISTS permission_type;
CREATE TYPE permission_type AS enum('pbl','grp','sol');

-- Дамп структуры для таблица wiki.articles
DROP SEQUENCE IF EXISTS articles_article_id_seq;
CREATE SEQUENCE IF NOT EXISTS articles_article_id_seq;

DROP TABLE IF EXISTS articles;
CREATE TABLE IF NOT EXISTS articles (
  article_id int unique not null DEFAULT nextval('articles_article_id_seq') primary key,
  author_id int NOT NULL references authors(author_id),
  article_title text NOT NULL,
  article_annotation text,
  article_html text NOT NULL,
  category_article_id int NOT NULL,
  template int DEFAULT NULL,
  permissions permission_type  NOT NULL DEFAULT 'pbl'
);

ALTER SEQUENCE articles_article_id_seq OWNED BY articles.article_id;

CREATE INDEX articles_article_id_idx ON articles (article_id);
CREATE INDEX articles_author_id_idx ON articles (author_id);
CREATE INDEX category_article_id ON articles (category_article_id);
CREATE INDEX template ON articles (template);
CREATE INDEX permissions ON articles (permissions);


-- Дамп структуры для таблица wiki.annotations
DROP TABLE IF EXISTS annotations;
CREATE TABLE IF NOT EXISTS annotations (
  article_id int NOT NULL references articles(article_id),
  annotation_text text NOT NULL,
  annotation_sha_hash varchar(66)  NOT NULL,
  PRIMARY KEY (annotation_sha_hash)
);

CREATE INDEX annotation_article_id ON annotations (article_id);



--ALTER TABLE products ADD CHECK (name <> '');
--ALTER TABLE products ADD CONSTRAINT some_name UNIQUE (product_no);
--ALTER TABLE products ADD FOREIGN KEY (product_group_id) REFERENCES product_groups;
--To add a not-null constraint, which cannot be written as a table constraint, use this syntax:
--
--ALTER TABLE products ALTER COLUMN product_no SET NOT NULL;


-- Дамп структуры для таблица wiki.files
DROP SEQUENCE IF EXISTS files_file_id_seq;
CREATE SEQUENCE IF NOT EXISTS files_file_id_seq;

DROP TABLE IF EXISTS files;
CREATE TABLE IF NOT EXISTS files (
  file_id int not null DEFAULT nextval('files_file_id_seq') primary key,
  author_id int NOT NULL references authors(author_id),
  file_create_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  file_inside_name varchar(66) NOT NULL,
  file_extension varchar(20) NOT NULL,
  file_name varchar(254) NOT NULL
);
ALTER SEQUENCE files_file_id_seq OWNED BY files.file_id;


CREATE INDEX file_create_date ON files (file_create_date);
CREATE INDEX file_extension ON files (file_extension);
CREATE INDEX file_name ON files (file_name);
CREATE INDEX files_author_id ON files (author_id);

-- Дамп данных таблицы wiki.files: ~0 rows (приблизительно)
/*!40000 ALTER TABLE files DISABLE KEYS */;
/*!40000 ALTER TABLE files ENABLE KEYS */;


DROP TYPE IF EXISTS files_kross_type;
CREATE TYPE files_kross_type AS enum('A','M');

-- Дамп структуры для таблица wiki.files_kroses
DROP TABLE IF EXISTS files_kroses;
CREATE TABLE IF NOT EXISTS files_kroses (
  file_id int not null references files(file_id),
  article_id int NOT NULL references articles(article_id),
  file_kros_create_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  file_kros_flag files_kross_type NOT NULL,
  PRIMARY KEY (file_id,article_id)
);

CREATE INDEX files_kroses_file_id ON files_kroses (file_id);
CREATE INDEX files_kroses_article_id ON files_kroses (article_id);
CREATE INDEX file_kros_create_date ON files_kroses (file_kros_create_date);
CREATE INDEX file_kros_flag ON files_kroses (file_kros_flag);

-- Дамп данных таблицы wiki.files_kroses: ~0 rows (приблизительно)
/*!40000 ALTER TABLE files_kroses DISABLE KEYS */;
/*!40000 ALTER TABLE files_kroses ENABLE KEYS */;


DROP TYPE IF EXISTS revision_type;
CREATE TYPE revision_type AS enum('A','N');


-- Дамп структуры для таблица wiki.revisions
DROP SEQUENCE IF EXISTS revisions_revision_id_seq;
CREATE SEQUENCE IF NOT EXISTS revisions_revision_id_seq;

DROP TABLE IF EXISTS revisions;
CREATE TABLE IF NOT EXISTS revisions (
  revision_id int unique not null DEFAULT nextval('revisions_revision_id_seq') primary key,
  article_id int NOT NULL references articles(article_id),
  author_id int NOT NULL references authors(author_id),
  revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revision_actual_flag revision_type NOT NULL,
  title_sha_hash varchar(66) NOT NULL,
  annotation_sha_hash varchar(66) NOT NULL,
  text_sha_hash varchar(66) NOT NULL
);
ALTER SEQUENCE revisions_revision_id_seq OWNED BY revisions.revision_id;


CREATE INDEX revisions_article_id ON files_kroses (article_id);
CREATE INDEX revisions_revision_date ON revisions (revision_date);
CREATE INDEX revisions_title_sha_hash ON revisions (title_sha_hash);
CREATE INDEX revisions_annotation_sha_hash ON revisions (annotation_sha_hash);
CREATE INDEX revisions_text_sha_hash ON revisions (text_sha_hash);
CREATE INDEX revisions_revision_actual_flag ON revisions (revision_actual_flag);
CREATE INDEX revisions_author_id ON revisions (author_id);



-- Дамп структуры для таблица wiki.texts
DROP TABLE IF EXISTS texts;
CREATE TABLE IF NOT EXISTS texts (
  article_id int NOT NULL references articles(article_id),
  text_sha_hash varchar(66) NOT NULL,
  text_html text NOT NULL,
  PRIMARY KEY (text_sha_hash)
);

CREATE INDEX texts_article_id ON texts (article_id);
CREATE INDEX texts_text_sha_hash ON texts (text_sha_hash);



-- Дамп структуры для таблица wiki.titles
DROP TABLE IF EXISTS titles;
CREATE TABLE IF NOT EXISTS titles (
  article_id int NOT NULL references articles(article_id),
  title_text text NOT NULL,
  title_sha_hash varchar(66) NOT NULL,
  PRIMARY KEY (title_sha_hash)
);

CREATE INDEX titles_article_id ON titles (article_id);


---------------------

--
-- TOC entry 2213 (class 0 OID 25085)
-- Dependencies: 182
-- Data for Name: articles; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO  authors (author_id, author_create, author_login, author_name, author_external, author_pass, author_phon, author_email, author_role) VALUES 
(1,	'2015-12-25 12:53:08',	'login',	'MyName And SurName',	'',	'$2b$12$.b9454ab5a22859b68bb4uvIvIvpREbnd9t2DJ7rqm1bwB/PrsH0.',	'1234-65432-4444',	'mail_0001@mail.com',	'admin');
ALTER SEQUENCE authors_author_id_seq OWNED BY authors.author_id;


--SELECT setval('articles_article_id_seq', (SELECT MAX(article_id) FROM articles) );
SELECT setval('authors_author_id_seq', COALESCE((SELECT MAX(author_id)+1 FROM authors), 1), false);
--ALTER SEQUENCE articles_article_id_seq START (SELECT MAX(article_id)+1 FROM articles) ;



INSERT INTO  articles (article_id, author_id, article_title, article_annotation, article_html, category_article_id, template, permissions) VALUES 
(1,	1, '0KHQv9C40YHQvtC6INCa0LDRgtC10LPQvtGA0LjQuSDRgdGC0LDRgtC10Lk=',	'0KHQv9C40YHQvtC6INCa0LDRgtC10LPQvtGA0LjQuSDRgdGC0LDRgtC10Lk=',	'PHA+0KHQv9C40YHQvtC6INCa0LDRgtC10LPQvtGA0LjQuSDRgdGC0LDRgtC10Lk8L3A+',	0,	'0',	'pbl'),
(2,	1, '0KHQu9GD0LbQtdCx0L3Ri9C1INGB0YLQsNGC0YzQuA==',	'0KHQu9GD0LbQtdCx0L3Ri9C1INGB0YLQsNGC0YzQuA==',	'PHA+0KHQu9GD0LbQtdCx0L3Ri9C1INGB0YLQsNGC0YzQuDwvcD4=',	1,	'0',	'pbl'),
(3,	1, '0KjQsNCx0LvQvtC90Ys=',	'0KjQsNCx0LvQvtC90Ys=',	'PHA+0KjQsNCx0LvQvtC90Ys8L3A+',	1,	'0',	'pbl'),
(4,	1, '0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90LDRjyDRgdGC0LDRgtGM0Y8=',	'0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90LDRjyDRgdGC0LDRgtGM0Y8=',	'PHA+0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90LDRjyDRgdGC0LDRgtGM0Y88L3A+',	1,	'0',	'pbl'),
(5,	1, '0JPQu9Cw0LLQvdCw0Y8g0YHRgtCw0YLRjNGPINGB0LDQudGC0LA=',	'0JPQu9Cw0LLQvdCw0Y8g0YHRgtCw0YLRjNGPINGB0LDQudGC0LA=',	'PHA+0JPQu9Cw0LLQvdCw0Y8g0YHRgtCw0YLRjNGPINGB0LDQudGC0LA8L3A+',	4,	'6',	'pbl'),
(6,	1, '0J7RgdC90L7QstC90L7QuSDRiNCw0LHQu9C+0L0g0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90L7QuSDRgdGC0YDQsNC90LjRhtGL',	'0J7RgdC90L7QstC90L7QuSDRiNCw0LHQu9C+0L0g0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90L7QuSDRgtGA0LDQvdC40YbRiw==',	'PCFET0NUWVBFIGh0bWw+DQo8aHRtbD4NCjxoZWFkPg0KPG1ldGEgY2hhcnNldD0iVVRGLTgiPg0KPHRpdGxlPlRvcm5hZG8gV2lraSBBZG1pbiBsYXllcjwvdGl0bGU+DQo8bGluayByZWw9InN0eWxlc2hlZXQiIGhyZWY9Ii9zdGF0aWMvd2lraS5jc3MiIHR5cGU9InRleHQvY3NzIj4NCjxsaW5rIHJlbD0iYWx0ZXJuYXRlIiBocmVmPSIvZmVlZCIgdHlwZT0iYXBwbGljYXRpb24vYXRvbSt4bWwiIA0KdGl0bGU9Int7YXJ0aWNsZS5hcnRpY2xlX3RpdGxlfX0iPg0KDQo8L2hlYWQ+DQo8Ym9keT4NCjxkaXYgaWQ9ImJvZHkiPg0KPGRpdiBpZD0iaGVhZGVyIj4NCjxkaXYgc3R5bGU9ImZsb2F0OnJpZ2h0Ij4NCg0KPGEgaHJlZj0iL2F1dGgvbG9naW4iPlNpZ24gaW48L2E+IHRvIGNvbXBvc2UvZWRpdA0KDQo8L2Rpdj4NCjxoMT48YSBocmVmPSIvIj7QndCwINCT0LvQsNCy0L3Rg9GOPC9hPjwvaDE+DQo8L2Rpdj4NCjwhLS0gdXNlciBJUzogTm9uZSAtLT4NCjxkaXYgaWQ9ImNvbnRlbnQiPg0KDQo8IS0tIG1vZHVsZXMgMTM3ICBhcnRpY2xlLmh0bWwgLS0+DQo8ZGl2IGNsYXNzPSJhcnRpY2xlIj4NCjxoMT48YSBocmVmPSJ7e2FydGljbGUuYXJ0aWNsZV9pZH19Ij57e2FydGljbGUuYXJ0aWNsZV90aXRsZX19PC9hPjwvaDE+DQo8ZGl2IGNsYXNzPSJib2R5Ij57e2FydGljbGUuYXJ0aWNsZV9hbm5vdGF0aW9ufX08L2Rpdj4NCjxkaXYgY2xhc3M9ImJvZHkiPg0KeyUgcmF3IGFydGljbGUuYXJ0aWNsZV9odG1sICV9DQo8YnI+DQo8IS0tIG1vZHVsZXMvZmlsZXNfbGlzdC5odG1sIC0tPg0Ke3tmaWxlTGlzdH19DQo8IS0tIC8gbW9kdWxlcy9maWxlc19saXN0Lmh0bWwgLS0+DQo8L2Rpdj4NCjxkaXYgY2xhc3M9ImFkbWluIj4NCls8YSBocmVmPSJ7e2FydGljbGUuYXJ0aWNsZV9pZH19Ij5FZGl0IHRoaXMgd2lraTwvYT5dDQpbPGEgaHJlZj0ie3thcnRpY2xlLmFydGljbGVfaWR9fSI+VmlldyBhbGwgcmV2aXNpb25zPC9hPl0NCjwvZGl2Pg0KPC9kaXY+DQoNCjwvZGl2Pg0KPC9kaXY+DQoNCjwvYm9keT4NCjwvaHRtbD4=',	3,	0,	'pbl');
--SELECT setval('articles_article_id_seq', (SELECT MAX(article_id) FROM articles) );
SELECT setval('articles_article_id_seq', COALESCE((SELECT MAX(article_id)+1 FROM articles), 1), false);
--ALTER SEQUENCE articles_article_id_seq START (SELECT MAX(article_id)+1 FROM articles) ;


INSERT INTO  annotations (article_id, annotation_text, annotation_sha_hash) VALUES 
(2,	'0KHQu9GD0LbQtdCx0L3Ri9C1INGB0YLQsNGC0YzQuA==',	'3312f2f071e0c4c50c9165159db773750761d6a9bbf73bacd2270d6d868d1dd0'),
(4,	'0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90LDRjyDRgdGC0LDRgtGM0Y8=',	'5bef2d09b4f5f2110373870af4c9c7e0ddc135fe029087508538fc950d5b97da'),
(1,	'0KHQv9C40YHQvtC6INCa0LDRgtC10LPQvtGA0LjQuSDRgdGC0LDRgtC10Lk=',	'8402d4bffd9334332c82c79ac1c226eba896aec279027172a4e1c0c29231766f'),
(3,	'0KjQsNCx0LvQvtC90Ys=',	'8c0f4c6dfae1b203f4f6f4ce4476c2dbf2077d91a6ab12ad290bb66328e8081c'),
(6,	'0J7RgdC90L7QstC90L7QuSDRiNCw0LHQu9C+0L0g0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90L7QuSDRgtGA0LDQvdC40YbRiw==',	'c9761801d393a57c1bf154f9ad58d01c5c6abf9b06272bfc6a7cf70d3e4532b7'),
(5,	'0JPQu9Cw0LLQvdCw0Y8g0YHRgtCw0YLRjNGPINGB0LDQudGC0LA=',	'cd0a31e15ed0f494158e78d79a554ee926a2583e56868a9cf3b7d53cbc207bff');



--
-- TOC entry 2221 (class 0 OID 25193)
-- Dependencies: 190
-- Data for Name: revisions; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO  revisions (revision_id, article_id, author_id, revision_date, revision_actual_flag, title_sha_hash, annotation_sha_hash, text_sha_hash) VALUES 
(1,	1,	1,	'2016-08-11 09:33:43',	'A',	'136e050397813d0297c61a5ab8ecb24928896a4b282f0a4be52de7bf19e2907d',	'8402d4bffd9334332c82c79ac1c226eba896aec279027172a4e1c0c29231766f',	'c41af4fe916911c79460ec66c912a82868bdaadca6fbeb5329953f8e3b074b15'),
(2,	2,	1,	'2016-08-11 09:34:11',	'A',	'9a28c9f82da29ef3ecc8052d88363a3b3bc0ae6e4c250743b17a27a4398c8a1a',	'3312f2f071e0c4c50c9165159db773750761d6a9bbf73bacd2270d6d868d1dd0',	'ff0917f405ec86faeff00de5eed8e26b9fea3680a2cbf5ae99aafa49bd324fb8'),
(3,	3,	1,	'2016-08-11 09:34:31',	'A',	'99d49ee10b9e1309e286af411756e97d90d11dc9763be58299fa89ae8c3fb6f2',	'8c0f4c6dfae1b203f4f6f4ce4476c2dbf2077d91a6ab12ad290bb66328e8081c',	'ee5c6e6d845e957e61f43fcc4919ad78452cd2fa770d61897042aa2e1c69766c'),
(4,	4,	1,	'2016-08-11 09:34:53',	'A',	'0e27a9d729935babb7f9489e627ea7fb83599136684370b3ff327269ff2d1b5f',	'5bef2d09b4f5f2110373870af4c9c7e0ddc135fe029087508538fc950d5b97da',	'a2bdf727661b4064802c9c1a4858d7fb07b6db7ef196e77c7367ac054ff99035'),
(5,	5,	1,	'2016-08-11 09:36:25',	'A',	'49f68ae49b1599586d02a26ffd33f3d9bd26bbf8f2b624efef7abd21151c7ded',	'cd0a31e15ed0f494158e78d79a554ee926a2583e56868a9cf3b7d53cbc207bff',	'9ab19d7ebab9c72a557be2fb02631f8eac77729515b23b9c47f9daa43a71cc50'),
(6,	6,	1,	'2016-10-04 19:30:37.173685',	'A',	'52c322298e8a7f517e34353ae10b5918b64019b6a53bfb3aa9532c3ccd22021d',	'c9761801d393a57c1bf154f9ad58d01c5c6abf9b06272bfc6a7cf70d3e4532b7',	'6494631c8b83ebc6d72a5add30f5a6899bd2fa2ff4de32ad85eb6536c93e217e');



INSERT INTO  texts (article_id, text_sha_hash, text_html) VALUES 
(5,	'9ab19d7ebab9c72a557be2fb02631f8eac77729515b23b9c47f9daa43a71cc50',	'eJyzKbC7MPnC7gsbLmy6sPfChov9ChcbLzYBGU0Xe8AcoMxOkICNfoEdAJZhHAQ='),
(4,	'a2bdf727661b4064802c9c1a4858d7fb07b6db7ef196e77c7367ac054ff99035',	'eJyzKbC7MOPC3ostF/ZdbLiw58KGi20XdlzYd2EvEG642K9wsfFiE5DRdLHnYr+NfoEdAA8eHvU='),
(1,	'c41af4fe916911c79460ec66c912a82868bdaadca6fbeb5329953f8e3b074b15',	'eJyzKbC7sPDC/gs7LjZe2Hdhl8KFWRc2XGy6sPXC5gv7LjZc2HFhp8LFRqAARHCnjX6BHQBpwyDx'),
(3,	'ee5c6e6d845e957e61f43fcc4919ad78452cd2fa770d61897042aa2e1c69766c',	'eJyzKbC7sOLChgsbL+y+sO/C3ovdNvoFdgCOSgx/'),
(2,	'ff0917f405ec86faeff00de5eed8e26b9fea3680a2cbf5ae99aafa49bd324fb8',	'eJwBJgDZ/zxwPtCh0LvRg9C20LXQsdC90YvQtSDRgdGC0LDRgtGM0Lg8L3A+3r0Xyw=='),
(6,	'6494631c8b83ebc6d72a5add30f5a6899bd2fa2ff4de32ad85eb6536c93e217e',	'eJyNU81q3DAQvi/sO0wEORVHLD20hLWhtCkUSlvItqWUElRrdi0iS4s0m2QxPvWeS899h5Br6Ds4b1TJa2+dbPpz0aDRfDPffKOZ7r14+3z26d0RFFTqbDyabi0KGW2JJCAvhPNIKXs/e5k8ZdFPijRmM+uMkBY+qlMFz2SpDGixRjflm/cQqJU5BYc6ZZ7WGn2BSAwKh/OUcU+CVM7PA/wg954BrZeYMsIL4vF+N4HQhKEe4RY/R5Q9SCyXWuUhnzVckC0fXZSawXjUMklZVQkXamk86OxJ+1DXsUgow/uOv1q5jlaqM1AyZfHOho4YiG7rattK2VxbQYdOLQrqMoqepVhRwbVdKMOyY7UwoMyUiwzIQm7LpfXIUSra0AgpW/0n2e8ELGt+NFfQfG9umqvmuvl5++32MqYIrCfZALWXJLDy6ODV8SG8sQYhSYbUc2sITU8wRpdWrsJUYPL4CUCvUPwEA2SuhfdB4M0ru09vV1klo6x/VHzIfJB/I/QuShhjqZ1rhHad7uDGo2ofnDiH+/C2mf06TtZld7vmcxXOE608DXququh+HZx13cXzvyMeYiXiNkRan/8p1FEYPlChPMRFiOp8+R/YB4WhW63DcpwpH+TxHXRLp7MPe/p/ztuV/wUBvlKN');
--

INSERT INTO  titles (article_id, title_text, title_sha_hash) VALUES 
(4,	'0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90LDRjyDRgdGC0LDRgtGM0Y8=',	'0e27a9d729935babb7f9489e627ea7fb83599136684370b3ff327269ff2d1b5f'),
(1,	'0KHQv9C40YHQvtC6INCa0LDRgtC10LPQvtGA0LjQuSDRgdGC0LDRgtC10Lk=',	'136e050397813d0297c61a5ab8ecb24928896a4b282f0a4be52de7bf19e2907d'),
(5,	'0JPQu9Cw0LLQvdCw0Y8g0YHRgtCw0YLRjNGPINGB0LDQudGC0LA=',	'49f68ae49b1599586d02a26ffd33f3d9bd26bbf8f2b624efef7abd21151c7ded'),
(3,	'0KjQsNCx0LvQvtC90Ys=',	'99d49ee10b9e1309e286af411756e97d90d11dc9763be58299fa89ae8c3fb6f2'),
(2,	'0KHQu9GD0LbQtdCx0L3Ri9C1INGB0YLQsNGC0YzQuA==',	'9a28c9f82da29ef3ecc8052d88363a3b3bc0ae6e4c250743b17a27a4398c8a1a'),
(6,	'0J7RgdC90L7QstC90L7QuSDRiNCw0LHQu9C+0L0g0JjQvdGE0L7RgNC80LDRhtC40L7QvdC90L7QuSDRgdGC0YDQsNC90LjRhtGL',	'52c322298e8a7f517e34353ae10b5918b64019b6a53bfb3aa9532c3ccd22021d');


SELECT setval('revisions_revision_id_seq', COALESCE((SELECT MAX(revision_id)+1 FROM revisions), 1), false);


--
-- TOC entry 2215 (class 0 OID 25107)
-- Dependencies: 184
-- Data for Name: authors; Type: TABLE DATA; Schema: public; Owner: postgres
--
----------------------------

DROP TYPE IF EXISTS group_status_def CASCADE;
CREATE TYPE group_status_def AS enum('pbl','shut');

DROP TABLE IF EXISTS groups CASCADE;

DROP SEQUENCE IF EXISTS groups_group_id_seq CASCADE;
CREATE SEQUENCE groups_group_id_seq;

CREATE TABLE IF NOT EXISTS groups (
  group_id int unique not null DEFAULT nextval('groups_group_id_seq') primary key,
  group_title varchar(254) NOT NULL,
  group_annotation text,
  group_status group_status_def  NOT NULL DEFAULT 'pbl',
  group_actual_flag revision_type NOT NULL,
  group_revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
ALTER SEQUENCE groups_group_id_seq OWNED BY groups.group_id;

CREATE INDEX groups_group_id_idx ON groups (group_id);
CREATE INDEX group_title ON groups (group_title);
CREATE INDEX group_status ON groups (group_status);
CREATE INDEX group_actual_flag ON groups (group_actual_flag);
CREATE INDEX group_revision_date ON groups (group_revision_date);


DROP TYPE IF EXISTS role_type CASCADE;
CREATE TYPE role_type AS enum('M','A');

DROP TABLE IF EXISTS members CASCADE;

CREATE TABLE IF NOT EXISTS members (
  group_id int NOT NULL references groups(group_id),
  author_id int NOT NULL references authors(author_id),
  member_role_type role_type NOT NULL,
  member_actual_flag revision_type NOT NULL,
  member_revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
  
);

CREATE INDEX members_group_id_idx ON members (group_id);
CREATE INDEX members_author_id_idx ON members (author_id);
CREATE INDEX member_role_type_idx ON members (member_role_type);
CREATE INDEX member_actual_flag_idx ON members (member_actual_flag);
CREATE INDEX member_revision_date_idx ON members (member_revision_date);


DROP TYPE IF EXISTS library_permission_type_def CASCADE;
CREATE TYPE library_permission_type_def AS enum('R','W');


DROP TABLE IF EXISTS librarys CASCADE;

CREATE TABLE IF NOT EXISTS librarys (
  group_id int NOT NULL references groups(group_id),
  article_id int NOT NULL references articles(article_id),
  library_permission_type library_permission_type_def NOT NULL,
  library_actual_flag revision_type NOT NULL,
  library_revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX librarys_group_id_idx ON librarys (group_id);
CREATE INDEX librarys_article_id_idx ON librarys (article_id);
CREATE INDEX library_permission_type_idx ON librarys (library_permission_type);
CREATE INDEX library_actual_flag_idx ON librarys (library_actual_flag);
CREATE INDEX library_revision_date_idx ON librarys (library_revision_date);


