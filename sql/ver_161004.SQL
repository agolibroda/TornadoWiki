-- повод ревизии - добавил  - отредактировал - удалил
DROP TYPE IF EXISTS revision_data_type CASCADE;
CREATE TYPE revision_data_type AS enum('I', 'U', 'D');

DROP TYPE IF EXISTS revision_actual_type;
CREATE TYPE revision_actual_type AS ENUM ( 'A', 'O' );

DROP TYPE IF EXISTS author_type;
CREATE TYPE author_type AS enum('admin','volunteer');

-- Дамп структуры для таблица wiki.authors
DROP SEQUENCE IF EXISTS authors_author_id_seq;
CREATE SEQUENCE IF NOT EXISTS authors_author_id_seq;


DROP TABLE IF EXISTS authors;
CREATE TABLE IF NOT EXISTS authors (
  author_id int unique not null DEFAULT nextval('authors_author_id_seq') primary key,
  author_create timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  author_login varchar(50) unique NOT NULL,
  author_email varchar(254) unique DEFAULT NULL,
  author_name varchar(254) DEFAULT NULL,
  author_surname varchar(50) DEFAULT NULL,
  author_pass varchar(70) DEFAULT NULL,
  author_phon varchar(50) DEFAULT NULL,
  author_role author_type NOT NULL DEFAULT 'volunteer'
);

CREATE INDEX authors_author_id ON authors (author_id);
CREATE INDEX authors_author_create_id ON authors (author_create);
CREATE INDEX authors_author_login_id ON authors (author_login);
CREATE INDEX authors_author_name_id ON authors (author_name);
CREATE INDEX authors_author_surname_id ON authors (author_surname);


CREATE INDEX authors_author_pass_id ON authors (author_pass);
CREATE INDEX authors_author_phon_id ON authors (author_phon);
CREATE INDEX authors_author_email_id ON authors (author_email);


DROP TABLE IF EXISTS revisions_authors;
CREATE TABLE IF NOT EXISTS revisions_authors (
  author_id int  NOT NULL references authors(author_id),
  author_create timestamp NOT NULL,
  author_login varchar(50) NOT NULL,
  author_name varchar(254) DEFAULT NULL,
  author_surname varchar(50) DEFAULT NULL,
  author_pass varchar(70) DEFAULT NULL,
  author_phon varchar(50) DEFAULT NULL,
  author_email varchar(254) DEFAULT NULL,
  author_role author_type NOT NULL DEFAULT 'volunteer',
  
  revisions_sha_hash character varying(66) NOT NULL  primary key,
  revision_actual_flag revision_actual_type NOT NULL,
  
  operation_flag revision_data_type NOT NULL,
  revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revision_author_id int NOT NULL references authors(author_id)
  
);

CREATE INDEX revisions_authors_author_id ON revisions_authors (author_id);
CREATE INDEX revisions_authors_author_create_id ON revisions_authors (author_create);
CREATE INDEX revisions_authors_author_login_id ON revisions_authors (author_login);
CREATE INDEX revisions_authors_author_name_id ON revisions_authors (author_name);
CREATE INDEX revisions_authors_author_surname_id ON revisions_authors (author_surname);

CREATE INDEX revisions_authors_author_pass_id ON revisions_authors (author_pass);
CREATE INDEX revisions_authors_author_phon_id ON revisions_authors (author_phon);
CREATE INDEX revisions_authors_author_email_id ON revisions_authors (author_email);

CREATE INDEX revisions_authors_articles_operation_flag_idx ON revisions_authors (operation_flag);
CREATE INDEX revisions_authors_articles_revision_date_idx ON revisions_authors (revision_date);
CREATE INDEX revisions_authors_articles_revision_author_id_idx ON revisions_authors (revision_author_id);
CREATE INDEX revisions_authors_revision_actual_flag_idx ON revisions_authors (revision_actual_flag);



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
  article_source text NOT NULL,
  article_category_id int NOT NULL,
  article_template_id int DEFAULT NULL,
  article_permissions permission_type  NOT NULL DEFAULT 'pbl'
  
);

ALTER SEQUENCE articles_article_id_seq OWNED BY articles.article_id;

CREATE INDEX articles_article_id_idx ON articles (article_id);
CREATE INDEX articles_author_id_idx ON articles (author_id);
CREATE INDEX articles_article_category_id ON articles (article_category_id);
CREATE INDEX articles_article_template_id_id ON articles (article_template_id);
CREATE INDEX articles_permissions_id ON articles (article_permissions);


DROP TABLE IF EXISTS revisions_articles;
CREATE TABLE IF NOT EXISTS revisions_articles (
  article_id int not null  references articles(article_id),
  author_id int NOT NULL references authors(author_id),
  article_title text NOT NULL,
  article_annotation text,
  article_source text NOT NULL,
  article_category_id int NOT NULL,
  article_template_id int DEFAULT NULL,
  article_permissions permission_type  NOT NULL DEFAULT 'pbl',
  
  revisions_sha_hash character varying(66) NOT NULL  primary key,
  revision_actual_flag revision_actual_type NOT NULL,
  
  operation_flag revision_data_type NOT NULL,
  revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revision_author_id int NOT NULL references authors(author_id)
  
);

CREATE INDEX revision_articles_article_id_idx ON revisions_articles (article_id);
CREATE INDEX revision_articles_author_id_idx ON revisions_articles (author_id);
CREATE INDEX revision_articles_article_category_id ON revisions_articles (article_category_id);
CREATE INDEX revision_articles_article_template_id_id ON revisions_articles (article_template_id);
CREATE INDEX revision_articles_permissions_id ON revisions_articles (article_permissions);

CREATE INDEX revision_articles_operation_flag_idx ON revisions_articles (operation_flag);
CREATE INDEX revision_articles_revision_date_idx ON revisions_articles (revision_date);
CREATE INDEX revision_articles_revision_author_id_idx ON revisions_articles (revision_author_id);



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

CREATE INDEX file_file_id ON files (file_id);
CREATE INDEX file_author_id ON files (author_id);
CREATE INDEX file_create_date_id ON files (file_create_date);
CREATE INDEX file_extension_id ON files (file_extension);
CREATE INDEX file_name_id ON files (file_name);


DROP TABLE IF EXISTS revisions_files;
CREATE TABLE IF NOT EXISTS revisions_files (
  file_id int not null references files(file_id),
  author_id int NOT NULL references authors(author_id),
  file_create_date timestamp NOT NULL,
  file_inside_name varchar(66) NOT NULL,
  file_extension varchar(20) NOT NULL,
  file_name varchar(254) NOT NULL,
  
  revisions_sha_hash character varying(66) NOT NULL  primary key,
  revision_actual_flag revision_actual_type NOT NULL,
  
  operation_flag revision_data_type NOT NULL,
  revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revision_author_id int NOT NULL references authors(author_id)
  
);

CREATE INDEX revision_files_file_id ON revisions_files (file_id);
CREATE INDEX revision_files_author_id ON revisions_files (author_id);
CREATE INDEX revision_files_create_date_id ON revisions_files (file_create_date);
CREATE INDEX revision_files_extension_id ON revisions_files (file_extension);
CREATE INDEX revision_files_name_id ON revisions_files (file_name);


CREATE INDEX revision_files_operation_flag_idx ON revisions_files (operation_flag);
CREATE INDEX revision_files_revision_date_idx ON revisions_files (revision_date);
CREATE INDEX revision_files_revision_author_id_idx ON revisions_files (revision_author_id);


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
CREATE INDEX file_kros_create_date_idx ON files_kroses (file_kros_create_date);
CREATE INDEX file_kros_flag_id ON files_kroses (file_kros_flag);


DROP TABLE IF EXISTS revisions_files_kroses;
CREATE TABLE IF NOT EXISTS revisions_files_kroses (
  file_id int not null references files(file_id),
  article_id int NOT NULL references articles(article_id),
  file_kros_create_date timestamp NOT NULL,
  file_kros_flag files_kross_type NOT NULL,
  
  revisions_sha_hash character varying(66) NOT NULL  primary key,
  revision_actual_flag revision_actual_type NOT NULL,
  
  operation_flag revision_data_type NOT NULL,
  revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revision_author_id int NOT NULL references authors(author_id)
);

CREATE INDEX revision_files_kroses_file_id ON revisions_files_kroses (file_id);
CREATE INDEX revision_files_kroses_article_id ON revisions_files_kroses (article_id);
CREATE INDEX revision_file_kros_create_date_idx ON revisions_files_kroses (file_kros_create_date);
CREATE INDEX revision_file_kros_flag_id ON revisions_files_kroses (file_kros_flag);


CREATE INDEX revision_files_kroses_operation_flag_idx ON revisions_files_kroses (operation_flag);
CREATE INDEX revision_files_kroses_revision_date_idx ON revisions_files_kroses (revision_date);
CREATE INDEX revision_files_kroses_revision_author_id_idx ON revisions_files_kroses (revision_author_id);
CREATE INDEX revision_files_kroses_revision_actual_flag_idx ON revisions_files_kroses (revision_actual_flag);



INSERT INTO  authors (author_id, author_create, author_login, author_name, author_surname, author_pass, author_phon, author_email, author_role) VALUES 
(1,	'2015-12-25 12:53:08',	'login',	'MyName',	'SurName',	'$2b$12$.b9454ab5a22859b68bb4uvIvIvpREbnd9t2DJ7rqm1bwB/PrsH0.',	'1234-65432-4444',	'mail_0001@mail.com',	'admin');
ALTER SEQUENCE authors_author_id_seq OWNED BY authors.author_id;


--SELECT setval('articles_article_id_seq', (SELECT MAX(article_id) FROM articles) );
SELECT setval('authors_author_id_seq', COALESCE((SELECT MAX(author_id)+1 FROM authors), 1), false);
--ALTER SEQUENCE articles_article_id_seq START (SELECT MAX(article_id)+1 FROM articles) ;

INSERT INTO  revisions_authors (author_id, author_create, author_login, author_name, author_surname, author_pass, author_phon, author_email, author_role, operation_flag, revision_author_id, revision_actual_flag, revisions_sha_hash) VALUES 
(1,	'2015-12-25 12:53:08',	'login',	'MyName',	'SurName',	'$2b$12$.b9454ab5a22859b68bb4uvIvIvpREbnd9t2DJ7rqm1bwB/PrsH0.',	'1234-65432-4444',	'mail_0001@mail.com',	'admin', 'I', 1, 'A', 'b9454ab5a22859b68bb4uvIvIvpREbnd9t2DJ7rqm1bwB');
ALTER SEQUENCE authors_author_id_seq OWNED BY authors.author_id;


INSERT INTO  articles (article_id, author_id, article_title, article_annotation, article_source, article_category_id, article_template_id, article_permissions) VALUES 
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
CREATE INDEX group_create_date_idx ON groups (group_create_date);
CREATE INDEX group_title_idx ON groups (group_title);
CREATE INDEX group_status_idx ON groups (group_status);



DROP TABLE IF EXISTS revisions_groups CASCADE;
CREATE TABLE IF NOT EXISTS revisions_groups (
  group_id int  references groups(group_id),
  author_id int NOT NULL references authors(author_id),
  group_create_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  group_title varchar(254) NOT NULL,
  group_annotation text,
  group_status group_status_def  NOT NULL DEFAULT 'pbl',
  
  revisions_sha_hash character varying(66) NOT NULL  primary key,
  revision_actual_flag revision_actual_type NOT NULL,
  
  operation_flag revision_data_type NOT NULL,
  revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revision_author_id int NOT NULL references authors(author_id)

);

CREATE INDEX revisions_groups_group_id_idx ON revisions_groups (group_id);
CREATE INDEX revisions_groups_author_id_idx ON revisions_groups (author_id);
CREATE INDEX revisions_groups_create_date_idx ON revisions_groups (group_create_date);
CREATE INDEX revisions_groups_title_idx ON revisions_groups (group_title);
CREATE INDEX revisions_groups_status_idx ON revisions_groups (group_status);

CREATE INDEX revision_group_operation_flag_idx ON revisions_groups (operation_flag);
CREATE INDEX revision_group_revision_date_idx ON revisions_groups (revision_date);
CREATE INDEX revision_group_revision_author_id_idx ON revisions_groups (revision_author_id);
CREATE INDEX revision_group_revision_actual_flag_idx ON revisions_groups (revision_actual_flag);


DROP TYPE IF EXISTS role_type CASCADE;
CREATE TYPE role_type AS enum('M','A');

DROP TABLE IF EXISTS members CASCADE;
CREATE TABLE IF NOT EXISTS members (
  group_id int NOT NULL references groups(group_id),
  author_id int NOT NULL references authors(author_id),
  member_role_type role_type NOT NULL,
  CONSTRAINT members_pkey PRIMARY KEY (group_id, author_id)
   
);


CREATE INDEX members_group_id_idx ON members (group_id);
CREATE INDEX members_author_id_idx ON members (author_id);
CREATE INDEX member_role_type_idx ON members (member_role_type);


DROP TABLE IF EXISTS revisions_members CASCADE;
CREATE TABLE IF NOT EXISTS revisions_members (
  group_id int NOT NULL references groups(group_id),
  author_id int NOT NULL references authors(author_id),
  member_role_type role_type NOT NULL,

  revisions_sha_hash character varying(66) NOT NULL  primary key,
  revision_actual_flag revision_actual_type NOT NULL,
  
  operation_flag revision_data_type NOT NULL,
  revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revision_author_id int NOT NULL references authors(author_id)

);
  
CREATE INDEX revision_members_group_id_idx ON revisions_members (group_id);
CREATE INDEX revision_members_author_id_idx ON revisions_members (author_id);
CREATE INDEX revision_members_member_role_type_idx ON revisions_members (member_role_type);

CREATE INDEX revision_members_operation_flag_idx ON revisions_members (operation_flag);
CREATE INDEX revision_members_revision_date_idx ON revisions_members (revision_date);
CREATE INDEX revision_members_revision_author_id_idx ON revisions_members (revision_author_id);
CREATE INDEX revision_members_revision_actual_flag_idx ON revisions_members (revision_actual_flag);


DROP TYPE IF EXISTS library_permission_type_def CASCADE;
CREATE TYPE library_permission_type_def AS enum('R','W');


DROP TABLE IF EXISTS librarys CASCADE;
CREATE TABLE IF NOT EXISTS librarys (
  group_id int NOT NULL references groups(group_id),
  article_id int NOT NULL references articles(article_id),
  library_permission_type library_permission_type_def NOT NULL,
  CONSTRAINT librarys_pkey PRIMARY KEY (group_id, article_id)
);

CREATE INDEX librarys_group_id_idx ON librarys (group_id);
CREATE INDEX librarys_article_id_idx ON librarys (article_id);
CREATE INDEX library_permission_type_idx ON librarys (library_permission_type);


DROP TABLE IF EXISTS revisions_librarys CASCADE;
CREATE TABLE IF NOT EXISTS revisions_librarys (
  group_id int NOT NULL references groups(group_id),
  article_id int NOT NULL references articles(article_id),
  library_permission_type library_permission_type_def NOT NULL,

  revisions_sha_hash character varying(66) NOT NULL  primary key,
  revision_actual_flag revision_actual_type NOT NULL,
  
  operation_flag revision_data_type NOT NULL,
  revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revision_author_id int NOT NULL references authors(author_id)
  );

CREATE INDEX revision_librarys_group_id_idx ON revisions_librarys (group_id);
CREATE INDEX revision_librarys_article_id_idx ON revisions_librarys (article_id);
CREATE INDEX revision_librarys_permission_type_idx ON revisions_librarys (library_permission_type);

CREATE INDEX revision_librarys_operation_flag_idx ON revisions_librarys (operation_flag);
CREATE INDEX revision_librarys_revision_date_idx ON revisions_librarys (revision_date);
CREATE INDEX revision_librarys_revision_author_id_idx ON revisions_librarys (revision_author_id);
CREATE INDEX revision_librarys_revision_actual_flag_idx ON revisions_librarys (revision_actual_flag);





