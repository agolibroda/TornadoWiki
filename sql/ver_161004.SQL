-- повод ревизии - добавил  - отредактировал - удалил
DROP TYPE IF EXISTS revision_data_type CASCADE;
CREATE TYPE revision_data_type AS enum('I','U', 'D');

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


DROP TABLE IF EXISTS revisions_authors;
CREATE TABLE IF NOT EXISTS revisions_authors (
  author_id int  NOT NULL references authors(author_id),
  author_create timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  author_login varchar(50) NOT NULL,
  author_name varchar(254) DEFAULT NULL,
  author_external varchar(50) DEFAULT NULL,
  author_pass varchar(70) DEFAULT NULL,
  author_phon varchar(50) DEFAULT NULL,
  author_email varchar(254) DEFAULT NULL,
  author_role author_type NOT NULL DEFAULT 'volunteer',
  
  actual_flag revision_data_type NOT NULL,
  revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revision_author_id int NOT NULL references authors(author_id),
  CONSTRAINT revisions_authors_pkey PRIMARY KEY (author_id, actual_flag, revision_date)
  
);



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


DROP TABLE IF EXISTS revision__articles;
CREATE TABLE IF NOT EXISTS revision__articles (
  article_id int unique not null DEFAULT nextval('articles_article_id_seq') primary key,
  author_id int NOT NULL references authors(author_id),
  article_title text NOT NULL,
  article_annotation text,
  article_html text NOT NULL,
  category_article_id int NOT NULL,
  template int DEFAULT NULL,
  permissions permission_type  NOT NULL DEFAULT 'pbl',
  
  actual_flag revision_data_type NOT NULL,
  revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revision_author_id int NOT NULL references authors(author_id),
  CONSTRAINT revision__articles_pkey PRIMARY KEY (article_id, author_id, actual_flag, revision_date)
  
);



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


DROP TABLE IF EXISTS revision__files;
CREATE TABLE IF NOT EXISTS revision__files (
  file_id int not null DEFAULT nextval('files_file_id_seq') primary key,
  author_id int NOT NULL references authors(author_id),
  file_create_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  file_inside_name varchar(66) NOT NULL,
  file_extension varchar(20) NOT NULL,
  file_name varchar(254) NOT NULL,
  
  actual_flag revision_data_type NOT NULL,
  revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revision_author_id int NOT NULL references authors(author_id),
  CONSTRAINT revision__files_pkey PRIMARY KEY (file_id, author_id, actual_flag, revision_date)
  
);


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


DROP TABLE IF EXISTS revision_files_kroses;
CREATE TABLE IF NOT EXISTS revision_files_kroses (
  file_id int not null references files(file_id),
  article_id int NOT NULL references articles(article_id),
  file_kros_create_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  file_kros_flag files_kross_type NOT NULL,
  
  actual_flag revision_data_type NOT NULL,
  revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revision_author_id int NOT NULL references authors(author_id),
  CONSTRAINT revision_files_kroses_pkey PRIMARY KEY (file_id, article_id, group_actual_flag, group_revision_date)
);




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


DROP TYPE IF EXISTS group_status_def CASCADE;
CREATE TYPE group_status_def AS enum('pbl','shut');


DROP SEQUENCE IF EXISTS groups_group_id_seq CASCADE;
CREATE SEQUENCE groups_group_id_seq;

DROP TABLE IF EXISTS groups CASCADE;
CREATE TABLE IF NOT EXISTS groups (
  group_id int unique not null DEFAULT nextval('groups_group_id_seq') primary key,
  author_id int NOT NULL references authors(author_id),  
  group_create_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  group_title varchar(254) NOT NULL,
  group_annotation text,
  group_status group_status_def  NOT NULL DEFAULT 'pbl'
);
ALTER SEQUENCE groups_group_id_seq OWNED BY groups.group_id;

CREATE INDEX groups_group_id_idx ON groups (group_id);
CREATE INDEX groups_author_id_idx ON groups (author_id);
CREATE INDEX group_title_idx ON groups (group_title);
CREATE INDEX group_status_idx ON groups (group_status);
CREATE INDEX group_create_date_idx ON groups (group_create_date);



DROP TABLE IF EXISTS revisions_groups CASCADE;
CREATE TABLE IF NOT EXISTS revisions_groups (
  group_id int  references groups(group_id),
  author_id int NOT NULL references authors(author_id),
  group_title varchar(254) NOT NULL,
  group_annotation text,
  group_status group_status_def  NOT NULL DEFAULT 'pbl',
  actual_flag revision_data_type NOT NULL,
  revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revision_author_id int NOT NULL references authors(author_id),
  CONSTRAINT revisions_groups_pkey PRIMARY KEY (group_id, author_id, group_actual_flag, group_revision_date)

);

CREATE INDEX revision_group_actual_flag ON revisions_groups (group_actual_flag);
CREATE INDEX revision_group_revision_date ON revisions_groups (group_revision_date);


DROP TYPE IF EXISTS role_type CASCADE;
CREATE TYPE role_type AS enum('M','A');

DROP TABLE IF EXISTS members CASCADE;
CREATE TABLE IF NOT EXISTS members (
  group_id int NOT NULL references groups(group_id),
  author_id int NOT NULL references authors(author_id),
  member_role_type role_type NOT NULL,
  CONSTRAINT members_pkey PRIMARY KEY (group_id, author_id)
   
);

DROP TABLE IF EXISTS revision_members CASCADE;
CREATE TABLE IF NOT EXISTS revision_members (
  group_id int NOT NULL references groups(group_id),
  author_id int NOT NULL references authors(author_id),
  member_role_type role_type NOT NULL,

  actual_flag revision_data_type NOT NULL,
  revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revision_author_id int NOT NULL references authors(author_id),
  CONSTRAINT revision_members_pkey PRIMARY KEY (group_id, author_id, actual_flag, revision_date)

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
  library_permission_type library_permission_type_def NOT NULL
  CONSTRAINT librarys_pkey PRIMARY KEY (group_id, article_id)
);

CREATE INDEX librarys_group_id_idx ON librarys (group_id);
CREATE INDEX librarys_article_id_idx ON librarys (article_id);
CREATE INDEX library_permission_type_idx ON librarys (library_permission_type);


DROP TABLE IF EXISTS revision_librarys CASCADE;
CREATE TABLE IF NOT EXISTS revision_librarys (
  group_id int NOT NULL references groups(group_id),
  article_id int NOT NULL references articles(article_id),
  library_permission_type library_permission_type_def NOT NULL,

  actual_flag revision_data_type NOT NULL,
  revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revision_author_id int NOT NULL references authors(author_id),
  CONSTRAINT revision_librarys_pkey PRIMARY KEY (group_id, article_id, actual_flag, revision_date)
  );

CREATE INDEX library_actual_flag_idx ON librarys (library_actual_flag);
CREATE INDEX library_revision_date_idx ON librarys (library_revision_date);





