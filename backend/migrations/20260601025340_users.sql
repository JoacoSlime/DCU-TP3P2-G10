-- Add migration script here
create extension if not exists "uuid-ossp";

-- # Entity schema.

-- Create `users` table.
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

-- Create `groups` table.
create table if not exists groups (
    id uuid not null primary key default (uuid_generate_v4()),
    name varchar(50) not null unique
);

-- Create `permissions` table.
create table if not exists permissions (
    id uuid not null primary key default (uuid_generate_v4()),
    name text not null unique
);


-- # Join tables.

-- Create `users_groups` table for many-to-many relationships between users and groups.
create table if not exists users_groups (
    user_id uuid not null references users(id) on delete cascade,
    group_id uuid not null references groups(id) on delete cascade,
    primary key (user_id, group_id)
);

create index if not exists users_groups_user_id_idx on users_groups(user_id);
create index if not exists users_groups_group_id_idx on users_groups(group_id);

-- Create `groups_permissions` table for many-to-many relationships between groups and permissions.
create table if not exists groups_permissions (
    group_id uuid not null references groups(id) on delete cascade,
    permission_id uuid not null references permissions(id) on delete cascade,
    primary key (group_id, permission_id)
);

create index if not exists groups_permissions_group_id_idx on groups_permissions(group_id);
create index if not exists groups_permissions_permission_id_idx on groups_permissions(permission_id);

-- # Fixture hydration.

-- Insert "admin" user.
insert into users (email, password)
values (
    'admin@admin.com',
    '$argon2id$v=19$m=19456,t=2,p=1$VE0e3g7DalWHgDwou3nuRA$uC6TER156UQpk0lNQ5+jHM0l5poVjPA1he/Tyn9J4Zw'
);

-- Insert "users" and "superusers" groups.
insert into groups (name) values ('collaborators');
insert into groups (name) values ('administrators');

-- Insert individual permissions.
insert into permissions (name) values ('collaborators.add');
insert into permissions (name) values ('collaborators.remove');
insert into permissions (name) values ('collaborators.list');
insert into permissions (name) values ('measures.add');
insert into permissions (name) values ('measures.remove');
insert into permissions (name) values ('spots.add');
insert into permissions (name) values ('spots.remove');

-- Insert group permissions.
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

-- Insert users into groups.
insert into users_groups (user_id, group_id)
values (
    (select id from users where email = 'admin@admin.com'),
    (select id from groups where name = 'collaborators')
), (
    (select id from users where email = 'admin@admin.com'),
    (select id from groups where name = 'administrators')
);
