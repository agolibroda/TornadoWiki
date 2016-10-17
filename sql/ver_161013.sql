
DROP TYPE IF EXISTS revision_type CASCADE;
CREATE TYPE revision_type AS enum('A','N', 'D');


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


DROP TYPE IF EXISTS permission_type CASCADE;
CREATE TYPE role_type AS enum('M','A');

DROP TABLE IF EXISTS members CASCADE;

CREATE TABLE IF NOT EXISTS members (
  group_id int NOT NULL references groups(group_id),
  user_id int NOT NULL references users(user_id),
  member_role_type role_type NOT NULL,
  member_actual_flag revision_type NOT NULL,
  member_revision_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
  
);

CREATE INDEX members_group_id_idx ON members (group_id);
CREATE INDEX members_user_id_idx ON members (user_id);
CREATE INDEX member_role_type_idx ON members (member_role_type);
CREATE INDEX member_actual_flag_idx ON members (member_actual_flag);
CREATE INDEX member_revision_date_idx ON members (member_revision_date);


DROP TYPE IF EXISTS library_permission_type_def CASCADE;
CREATE TYPE library_permission_type_def AS enum('R','W');


DROP TABLE IF EXISTS librarys CASCADE;

CREATE SEQUENCE librarys_library_id_seq;
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
