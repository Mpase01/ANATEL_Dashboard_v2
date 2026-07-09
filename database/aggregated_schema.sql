-- Aggregated ANATEL Dashboard schema.
-- This table keeps the dashboard cuts needed for analysis while reducing
-- storage compared to raw detailed ANATEL records.

create table if not exists aggregated_subscription_records (
    id bigserial primary key,
    provider_id bigint not null references providers(id),
    import_batch_id bigint not null references import_batches(id),
    import_file_id bigint not null references import_files(id),

    period date not null,
    cnpj varchar(14) not null,
    company_name text not null,
    municipality_code varchar(7) not null,
    municipality_name text not null,
    state char(2) not null,
    technology text not null,
    access_medium text not null,
    person_type text not null,
    subscriptions_count bigint not null,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint ck_aggregated_subscription_records_count check (subscriptions_count > 0),
    constraint uq_aggregated_subscription_records_key unique (
        period,
        cnpj,
        company_name,
        municipality_code,
        municipality_name,
        state,
        technology,
        access_medium,
        person_type
    )
);

create index if not exists idx_aggregated_subscription_records_provider_period
    on aggregated_subscription_records (provider_id, period);

create index if not exists idx_aggregated_subscription_records_period
    on aggregated_subscription_records (period);

create index if not exists idx_aggregated_subscription_records_state
    on aggregated_subscription_records (state);

create index if not exists idx_aggregated_subscription_records_municipality
    on aggregated_subscription_records (municipality_code);

create index if not exists idx_aggregated_subscription_records_technology
    on aggregated_subscription_records (technology);

create index if not exists idx_aggregated_subscription_records_access_medium
    on aggregated_subscription_records (access_medium);

create index if not exists idx_aggregated_subscription_records_person_type
    on aggregated_subscription_records (person_type);

revoke all on table aggregated_subscription_records from anon, authenticated;

alter table aggregated_subscription_records enable row level security;
