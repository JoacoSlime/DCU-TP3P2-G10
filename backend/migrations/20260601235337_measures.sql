create table if not exists measures (
    id uuid not null primary key default (uuid_generate_v4()),

    -- relaciones
    spot_id uuid not null references spots(id) on delete cascade,
    collaborator_id uuid not null references users(id) on delete restrict,

    -- timestamps
    created_at timestamptz not null default now(),

    -- valores numericos base
    items_per_m2 numeric(12, 4) not null,
    weight numeric(12, 4) not null,
    area numeric(12, 4) not null,

    -- materiales contados
    pet int not null default 0,
    pead int not null default 0,
    pebd int not null default 0,
    pvc int not null default 0,
    pp int not null default 0,
    ps int not null default 0,
    pa int not null default 0,
    other int not null default 0,

    -- índices
    ihr_plata numeric(10, 4) not null,
    ibirp numeric(10, 4) not null,

    -- checks
    constraint measures_nonnegative_counts_chk check (
        pet >= 0 and pead >= 0 and pebd >= 0 and pvc >= 0 and
        pp >= 0 and ps >= 0 and pa >= 0 and other >= 0
    ),
    constraint measures_nonnegative_base_chk check (
        items_per_m2 >= 0 and weight >= 0 and area > 0
    )
);

create index if not exists measures_spot_id_idx on measures(spot_id);
create index if not exists measures_collaborator_id_idx on measures(collaborator_id);
create index if not exists measures_created_at_idx on measures(created_at);
