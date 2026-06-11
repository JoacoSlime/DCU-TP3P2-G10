create extension if not exists "uuid-ossp";

create table
    "users" (
        id uuid not null primary key default (uuid_generate_v4()),
        email varchar(255) not null unique,
        password varchar(100) not null,
        name varchar(50),
        surname varchar(50),
        generation_token varchar(100) unique
    );

create index users_email_idx on users (email);

create table if not exists groups (
    id uuid not null primary key default (uuid_generate_v4()),
    name varchar(50) not null unique
);

create table if not exists permissions (
    id uuid not null primary key default (uuid_generate_v4()),
    name text not null unique
);

create table if not exists users_groups (
    user_id uuid not null references users(id) on delete cascade,
    group_id uuid not null references groups(id) on delete cascade,
    primary key (user_id, group_id)
);

create index if not exists users_groups_user_id_idx on users_groups(user_id);
create index if not exists users_groups_group_id_idx on users_groups(group_id);

create table if not exists groups_permissions (
    group_id uuid not null references groups(id) on delete cascade,
    permission_id uuid not null references permissions(id) on delete cascade,
    primary key (group_id, permission_id)
);

create index if not exists groups_permissions_group_id_idx on groups_permissions(group_id);
create index if not exists groups_permissions_permission_id_idx on groups_permissions(permission_id);

insert into groups (name) values ('collaborators');
insert into groups (name) values ('administrators');

insert into permissions (name) values ('collaborators.add');
insert into permissions (name) values ('collaborators.remove');
insert into permissions (name) values ('collaborators.list');
insert into permissions (name) values ('measures.add');
insert into permissions (name) values ('measures.remove');
insert into permissions (name) values ('spots.add');
insert into permissions (name) values ('spots.remove');

insert into groups_permissions (group_id, permission_id)
values (
    (select id from groups where name = 'collaborators'),
    (select id from permissions where name = 'measures.add')
), (
    (select id from groups where name = 'collaborators'),
    (select id from permissions where name = 'spots.add')
), (
    (select id from groups where name = 'administrators'),
    (select id from permissions where name = 'collaborators.add')
), (
    (select id from groups where name = 'administrators'),
    (select id from permissions where name = 'collaborators.remove')
), (
    (select id from groups where name = 'administrators'),
    (select id from permissions where name = 'collaborators.list')
), (
    (select id from groups where name = 'administrators'),
    (select id from permissions where name = 'measures.remove')
), (
    (select id from groups where name = 'administrators'),
    (select id from permissions where name = 'spots.remove')
);
