create table if not exists spots (
    id uuid not null primary key default (uuid_generate_v4()),
    title varchar(255) not null unique,
    latitude  numeric(9, 6)  not null,
    longitude numeric(10, 6) not null
);

create index if not exists spots_latitude_idx on spots(latitude);
create index if not exists spots_longitude_idx on spots(longitude);
