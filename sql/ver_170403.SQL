-- повод ревизии - добавил  - отредактировал - удалил

-- create extension pgcrypto;

DROP TYPE IF EXISTS data_type CASCADE;
CREATE TYPE data_type AS enum('I', 'U', 'D');

DROP TYPE IF EXISTS actual_type;
CREATE TYPE actual_type AS ENUM ( 'A', 'O' );

DROP TYPE IF EXISTS author_type;
CREATE TYPE author_type AS enum('admin','volunteer');

-- Дамп структуры для таблица wiki.authors
DROP SEQUENCE IF EXISTS authors_author_id_seq;
CREATE SEQUENCE IF NOT EXISTS authors_author_id_seq;

DROP TABLE IF EXISTS authors;
CREATE TABLE IF NOT EXISTS authors (
  author_id int  NOT NULL primary key,
  author_create timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  author_login varchar(50) NOT NULL,
  author_name varchar(254) DEFAULT NULL,
  author_surname varchar(50) DEFAULT NULL,
  author_pass varchar(70) DEFAULT NULL,
  author_phon varchar(50) DEFAULT NULL,
  author_email varchar(254) DEFAULT NULL,
  author_role author_type NOT NULL DEFAULT 'volunteer',
  
  sha_hash character varying(66) NOT NULL,
  actual_flag actual_type NOT NULL,
  
  operation_flag data_type NOT NULL,
  operation_timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revisions_author_id int NOT NULL 
  
);

CREATE FUNCTION trigger_authors_before_lns () RETURNS trigger AS $$ 
BEGIN 
      If  NEW.author_id = 0 OR NEW.author_id IS NULL then 
      NEW.article_id = nextval('authors_author_id_seq');
      end if;

return NEW;
END; 
$$ LANGUAGE  plpgsql;

-- Создание триггера
CREATE TRIGGER author_bi 
BEFORE INSERT ON authors FOR EACH ROW 
EXECUTE PROCEDURE trigger_authors_before_lns ();


CREATE INDEX authors_author_id ON authors (author_id);
CREATE INDEX authors_author_create_id ON authors (author_create);
CREATE INDEX authors_author_login_id ON authors (author_login);
CREATE INDEX authors_author_name_id ON authors (author_name);
CREATE INDEX authors_author_surname_id ON authors (author_surname);

CREATE INDEX authors_author_pass_id ON authors (author_pass);
CREATE INDEX authors_author_phon_id ON authors (author_phon);
CREATE INDEX authors_author_email_id ON authors (author_email);

CREATE INDEX authors_articles_operation_flag_idx ON authors (operation_flag);

CREATE INDEX authors_sha_hash_idx ON authors (sha_hash);
CREATE INDEX authors_operation_timestamp_idx ON authors (operation_timestamp);
CREATE INDEX authors_revisions_author_id_idx ON authors (revisions_author_id);
CREATE INDEX authors_actual_flag_idx ON authors (actual_flag);



DROP TYPE IF EXISTS permission_type;
CREATE TYPE permission_type AS enum('pbl','grp','sol');

-- Дамп структуры для таблица wiki.articles
DROP SEQUENCE IF EXISTS articles_article_id_seq;
CREATE SEQUENCE IF NOT EXISTS articles_article_id_seq;


DROP TABLE IF EXISTS articles;
CREATE TABLE IF NOT EXISTS articles (
  article_id int not null   primary key,
  article_title character varying(254) NOT NULL,
  article_link character varying(254) NOT NULL,
  article_annotation text,
  article_source text NOT NULL,
  article_category_id int NOT NULL,
  article_template_id int DEFAULT NULL,
  article_permissions permission_type  NOT NULL DEFAULT 'pbl',
  
  sha_hash character varying(66) NOT NULL,
  actual_flag actual_type NOT NULL,
  
  operation_flag data_type NOT NULL,
  operation_timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revisions_author_id int NOT NULL references authors(author_id)
  
);

CREATE FUNCTION trigger_articles_before_lns () RETURNS trigger AS $$ 
BEGIN 
      If  NEW.article_id = 0 OR NEW.article_id IS NULL then 
      NEW.article_id = nextval('articles_article_id_seq');
      end if;

return NEW;
END; 
$$ LANGUAGE  plpgsql;

-- Создание триггера
CREATE TRIGGER articles_bi 
BEFORE INSERT ON articles FOR EACH ROW 
EXECUTE PROCEDURE trigger_articles_before_lns ();


CREATE INDEX articles_article_id_idx ON articles (article_id);
CREATE INDEX articles_article_link_idx ON articles (article_link);
CREATE INDEX articles_article_category_id ON articles (article_category_id);
CREATE INDEX articles_article_template_id_id ON articles (article_template_id);
CREATE INDEX articles_permissions_id ON articles (article_permissions);

CREATE INDEX articles_operation_flag_idx ON articles (operation_flag);
CREATE INDEX articles_operation_timestamp_idx ON articles (operation_timestamp);
CREATE INDEX articles_revisions_author_id_idx ON articles (revisions_author_id);



-- Дамп структуры для таблица wiki.files
DROP SEQUENCE IF EXISTS files_file_id_seq;
CREATE SEQUENCE IF NOT EXISTS files_file_id_seq;

DROP TABLE IF EXISTS files;
CREATE TABLE IF NOT EXISTS files (
  file_id int not null  primary key,
  file_create_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  file_inside_name varchar(66) NOT NULL,
  file_extension varchar(20) NOT NULL,
  file_name varchar(254) NOT NULL,
  
  sha_hash character varying(66) NOT NULL,
  actual_flag actual_type NOT NULL,
  
  operation_flag data_type NOT NULL,
  operation_timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revisions_author_id int NOT NULL references authors(author_id)
  
);

CREATE FUNCTION trigger_files_before_lns () RETURNS trigger AS $$ 
BEGIN 
      If  NEW.file_id = 0 OR NEW.file_id IS NULL then 
      NEW.file_id = nextval('files_file_id_seq');
      end if;

return NEW;
END; 
$$ LANGUAGE  plpgsql;

-- Создание триггера
CREATE TRIGGER files_bi 
BEFORE INSERT ON files FOR EACH ROW 
EXECUTE PROCEDURE trigger_files_before_lns ();


CREATE INDEX files_file_id ON files (file_id);
CREATE INDEX files_create_date_id ON files (file_create_date);
CREATE INDEX files_extension_id ON files (file_extension);
CREATE INDEX files_name_id ON files (file_name);


CREATE INDEX files_operation_flag_idx ON files (operation_flag);
CREATE INDEX files_date_idx ON files (operation_timestamp);
CREATE INDEX files_revisions_author_id_idx ON files (revisions_author_id);


DROP TYPE IF EXISTS files_kross_type;
CREATE TYPE files_kross_type AS enum('A','M');

-- Дамп структуры для таблица wiki.files_kroses
DROP TABLE IF EXISTS files_kroses;
CREATE TABLE IF NOT EXISTS files_kroses (
  file_id int not null references files(file_id),
  article_id int NOT NULL references articles(article_id),
  file_kros_create_date timestamp NOT NULL,
  file_kros_flag files_kross_type NOT NULL,
  
  sha_hash character varying(66) NOT NULL  primary key,
  actual_flag actual_type NOT NULL,
  
  operation_flag data_type NOT NULL,
  operation_timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revisions_author_id int NOT NULL references authors(author_id)
);


CREATE INDEX files_kroses_file_id ON files_kroses (file_id);
CREATE INDEX files_kroses_article_id ON files_kroses (article_id);
CREATE INDEX file_kros_create_date_idx ON files_kroses (file_kros_create_date);
CREATE INDEX file_kros_flag_id ON files_kroses (file_kros_flag);


CREATE INDEX files_kroses_operation_flag_idx ON files_kroses (operation_flag);
CREATE INDEX files_kroses_operation_timestamp_idx ON files_kroses (operation_timestamp);
CREATE INDEX files_kroses_revisions_author_id_idx ON files_kroses (revisions_author_id);
CREATE INDEX files_kroses_actual_flag_idx ON files_kroses (actual_flag);





INSERT INTO  authors (author_id, author_create, author_login, author_name, author_surname, author_pass, author_phon, author_email, author_role, operation_flag, revisions_author_id, actual_flag, sha_hash) VALUES 
(1,	'2015-12-25 12:53:08',	'login',	'MyName',	'SurName',	'$2b$12$.b9454ab5a22859b68bb4uvIvIvpREbnd9t2DJ7rqm1bwB/PrsH0.',	'1234-65432-4444',	'mail_0001@mail.com',	'admin', 'I', 1, 'A', 'b9454ab5a22859b68bb4uvIvIvpREbnd9t2DJ7rqm1bwB');

--SELECT setval('articles_article_id_seq', (SELECT MAX(article_id) FROM articles) );
SELECT setval('authors_author_id_seq', COALESCE((SELECT MAX(author_id)+1 FROM authors), 1), false);
--ALTER SEQUENCE articles_article_id_seq START (SELECT MAX(article_id)+1 FROM articles) ;
ALTER SEQUENCE authors_author_id_seq OWNED BY authors.author_id;



INSERT INTO articles (article_id, article_title, article_link, article_annotation, article_source, article_category_id, article_template_id, article_permissions, sha_hash, actual_flag, operation_flag, operation_timestamp, revisions_author_id) VALUES (6, 'Главная статья сайта', 'главная_статья_сайта', 'Главная статья сайта - что будет на главной странице сайта?', 'eJyzKbC7MPnC7gsbLmy6sPfChov9ChcbLzZdbAAK7L2w42LbhQ1AASBn58UmIPPCfqDMvgtbL+wCc9UKS/NLrEPyi8IzszMhHJukIgV9O14utbyk4gJrG/0COwCyQzSm', 3, 5, 'pbl', '849c4af9da930987ec5e1f7f80af9c3bb612de4caed11fb62db74949f03a6a41', 'A', 'I', '2017-03-23 18:47:28.45462', 1);
INSERT INTO articles (article_id, article_title, article_link, article_annotation, article_source, article_category_id, article_template_id, article_permissions, sha_hash, actual_flag, operation_flag, operation_timestamp, revisions_author_id) VALUES (3, 'Информационные статьи', 'информационные_статьи', 'Категория - Информационные статьи', 'eJwly7ENgzAABdFVXNFFDABiGAYgjiA9IEQKGIAqM7hBshA2K9zfCEdprnpX2oovF14DjoBnz5q6tYV5GH00Ek2K4yCym+z1fnYFG0ETUT0nTnOaYlqDlkQ0/LxGrfg/L3Nb3asDPc0=', 1, 5, 'pbl', '665350b869896eaaec57c3c068d790be2f31b8502a1d8c0ed46776fbb884b634', 'A', 'I', '2017-03-23 18:30:30.98642', 1);
INSERT INTO articles (article_id, article_title, article_link, article_annotation, article_source, article_category_id, article_template_id, article_permissions, sha_hash, actual_flag, operation_flag, operation_timestamp, revisions_author_id) VALUES (2, 'Служебные статьи', 'служебные_статьи', 'Категория - Служебные статьи', 'eJyzKbC7MOXC7ov9ChfbL2y9sPnCPoULey82X9gGJLvV8pKKC6wV1ApL80usLywEKgNJbL2wESR5YavCxcaLTRc2XGy62HNhB0SRTVKRgr4dL9eFfRf2X9hxsfHChgt7L+y4sNVGv8AOAEchPeU=', 1, 5, 'pbl', 'a6e13583c2d7ccd978828a6db7feb85fe35f4124a57ed72f0d95abd98d91b891', 'A', 'I', '2017-03-23 18:28:56.856951', 1);
INSERT INTO articles (article_id, article_title, article_link, article_annotation, article_source, article_category_id, article_template_id, article_permissions, sha_hash, actual_flag, operation_flag, operation_timestamp, revisions_author_id) VALUES (4, 'Шаблоны', 'шаблоны', 'Категория  - Шаблоны', 'eJyzKbC7sPxi04V9CkBiw4VdF/Zd2KqgVliaX2J9YQVQYOOF3UChvRe7IWI2+gV2ABH9HNs=', 1, 5, 'pbl', 'a713cf338b87ed943ccd9955206e18c9a1d0b7bcbcb1c18765faff99a3ce6e29', 'A', 'I', '2017-03-23 18:31:31.116259', 1);
INSERT INTO articles (article_id, article_title, article_link, article_annotation, article_source, article_category_id, article_template_id, article_permissions, sha_hash, actual_flag, operation_flag, operation_timestamp, revisions_author_id) VALUES (1, 'Список Категорий статей', 'список_категорий_статей', 'Начальный список категрий - что бы можно было категоризировать статьи', 'eJx9jsENwjAUQ++VukNO3FAHIOowHQBFsAClCJDKCjBDK1TUkqasYG+EAxwQBy5f+fGzv63LccEDPUs0COjRGT3fH3c0Jg5u0eGKiRvpg5kti7Vb2MzlaZImVglnMQf5PU8IrJXxa7PFymTi5zHds8JNWvuBWQoVLvcXqFuBu5d9lLrXPqnhPwuPKtHCR5B1bPgEeWiE/A==', 1, 5, 'pbl', 'ff3e6cdd19859e807b44f01fd725b6a151cb937e7c3901a20f692b935fbe6104', 'A', 'I', '2017-03-23 18:25:05.885938', 1);
INSERT INTO articles (article_id, article_title, article_link, article_annotation, article_source, article_category_id, article_template_id, article_permissions, sha_hash, actual_flag, operation_flag, operation_timestamp, revisions_author_id) VALUES (5, 'Основной шаблон Информационной страницы', 'основной_шаблон_информационной_страницы', 'Основной шаблон Информационной страницы собственной персоной!', 'eJyNVMtqGzEU3Qf8DzeCrIojTBctwTObJoVCaQNxW0opRhlde4Q10iBdxzHGq+67ybr/ELot/YfJH1WahzuJ08dmLjrSOfdxpBkfnr59Mfl4fgY5FTodHIx3EYWMsUASkOXCeaSEvZu8HD5nESdFGtOJdR/UQo15swy4VmYBDnXCPK01+hyRGOQOZwnjngSpjK8C5TjzngGtS0wY4TXxuL4vIDShM4Jwx58hyo4kylKrLOhZwwXZ4sl1oRkMDupKErbZCBdyaTxu47Te2G5jkpCGdw1eWrmOUaorUDJhcc36QDyIbgfVbSVspq2gE6fmOTWKmyNQM8iWzqGh6dKjg6NtnUp05ZfovDVCTyX6xZRsydLzFoJT4RcwseWYi04Otcc9DbGknGs7V4alF2puQJlIAbKQ2aK0HjlKRY2AkR2fh9JrW0fpby2WVt+qW6huqh/VbfW9+nn35e5rVAvTGaU91uFwCHVHry5O4I01CMNhf0SZNRS6bkcbTxdWLoP7MHr6DKBzIt6tHjPTwvtgZLPLHpa376CS0b4/OtuvvKffGLrPEsZYqu9PpLad7vHqQTqxgod0b5cua/wZX7r0ft98psJ3qpWnXtebTYRfB3C7bc/zvzMeq0vIIpo/OPj0z1GdhZsAlCsPq/qVivTz/9DeKwz9ah2e4ZXyYUC+pe7KaePjSPeieP0v+QXedm0o', 4, 5, 'pbl', '1c0205a3970f770cdeef9cd6b99c0c3079001245e96303bd2d41859c0aa396fe', 'A', 'U', '2017-03-23 22:06:28.471117', 1);


DROP TYPE IF EXISTS group_status_def CASCADE;
CREATE TYPE group_status_def AS enum('pbl','shut');


DROP SEQUENCE IF EXISTS groups_group_id_seq CASCADE;
CREATE SEQUENCE groups_group_id_seq;


DROP TABLE IF EXISTS groups CASCADE;
CREATE TABLE IF NOT EXISTS groups (
  group_id int NOT NULL   primary key,
  author_id int NOT NULL references authors(author_id),
  group_create_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  group_title varchar(254) NOT NULL,
  group_annotation text,
  group_status group_status_def  NOT NULL DEFAULT 'pbl',
  
  sha_hash character varying(66) NOT NULL,
  actual_flag actual_type NOT NULL,
  
  operation_flag data_type NOT NULL,
  operation_timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revisions_author_id int NOT NULL references authors(author_id)

);

CREATE FUNCTION trigger_groups_before_lns () RETURNS trigger AS $$ 
BEGIN 
      If  NEW.group_id = 0 OR NEW.group_id IS NULL then 
      NEW.group_id = nextval('groups_group_id_seq');
      end if;

return NEW;
END; 
$$ LANGUAGE  plpgsql;

-- Создание триггера
CREATE TRIGGER groups_bi 
BEFORE INSERT ON groups FOR EACH ROW 
EXECUTE PROCEDURE trigger_groups_before_lns ();


CREATE INDEX groups_group_id_idx ON groups (group_id);
CREATE INDEX groups_author_id_idx ON groups (author_id);
CREATE INDEX groups_create_date_idx ON groups (group_create_date);
CREATE INDEX groups_title_idx ON groups (group_title);
CREATE INDEX groups_status_idx ON groups (group_status);

CREATE INDEX group_operation_flag_idx ON groups (operation_flag);
CREATE INDEX group_operation_timestamp_idx ON groups (operation_timestamp);
CREATE INDEX group_revisions_author_id_idx ON groups (revisions_author_id);
CREATE INDEX group_actual_flag_idx ON groups (actual_flag);


DROP TYPE IF EXISTS role_type CASCADE;
CREATE TYPE role_type AS enum('M','A');


DROP TABLE IF EXISTS members CASCADE;
CREATE TABLE IF NOT EXISTS members (
  group_id int NOT NULL references groups(group_id),
  author_id int NOT NULL references authors(author_id),
  member_role_type role_type NOT NULL,

  sha_hash character varying(66) NOT NULL  primary key,
  actual_flag actual_type NOT NULL,
  
  operation_flag data_type NOT NULL,
  operation_timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revisions_author_id int NOT NULL references authors(author_id)

);
  
CREATE INDEX members_group_id_idx ON members (group_id);
CREATE INDEX members_author_id_idx ON members (author_id);
CREATE INDEX members_member_role_type_idx ON members (member_role_type);

CREATE INDEX members_operation_flag_idx ON members (operation_flag);
CREATE INDEX members_operation_timestamp_idx ON members (operation_timestamp);
CREATE INDEX members_revisions_author_id_idx ON members (revisions_author_id);
CREATE INDEX members_actual_flag_idx ON members (actual_flag);


DROP TYPE IF EXISTS library_permission_type_def CASCADE;
CREATE TYPE library_permission_type_def AS enum('R','W');


DROP TABLE IF EXISTS librarys CASCADE;
CREATE TABLE IF NOT EXISTS librarys (
  group_id int NOT NULL references groups(group_id),
  article_id int NOT NULL references articles(article_id),
  library_permission_type library_permission_type_def NOT NULL,

  sha_hash character varying(66) NOT NULL  primary key,
  actual_flag actual_type NOT NULL,
  
  operation_flag data_type NOT NULL,
  operation_timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revisions_author_id int NOT NULL references authors(author_id)
  );

CREATE INDEX librarys_group_id_idx ON librarys (group_id);
CREATE INDEX librarys_article_id_idx ON librarys (article_id);
CREATE INDEX librarys_permission_type_idx ON librarys (library_permission_type);

CREATE INDEX librarys_operation_flag_idx ON librarys (operation_flag);
CREATE INDEX librarys_operation_timestamp_idx ON librarys (operation_timestamp);
CREATE INDEX librarys_revisions_author_id_idx ON librarys (revisions_author_id);
CREATE INDEX librarys_actual_flag_idx ON librarys (actual_flag);





