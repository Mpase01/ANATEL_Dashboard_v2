-- ANATEL Dashboard - initial PostgreSQL schema
-- This schema is based on the real ANATEL CSV structure analyzed in July 2026.
-- It is designed for PostgreSQL/Supabase and keeps direct database access in the backend.

create table if not exists providers (
    id bigserial primary key,
    cnpj varchar(14) not null unique,
    primary_name text not null,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists provider_aliases (
    id bigserial primary key,
    provider_id bigint not null references providers(id) on delete cascade,
    alias_name text not null,
    created_at timestamptz not null default now(),
    constraint uq_provider_alias unique (provider_id, alias_name)
);

create table if not exists import_batches (
    id bigserial primary key,
    status text not null default 'pending',
    started_at timestamptz not null default now(),
    finished_at timestamptz,
    rows_read bigint not null default 0,
    rows_inserted bigint not null default 0,
    rows_updated bigint not null default 0,
    rows_skipped bigint not null default 0,
    error_message text,
    constraint ck_import_batches_status check (
        status in ('pending', 'running', 'completed', 'failed', 'skipped')
    )
);

create table if not exists import_files (
    id bigserial primary key,
    import_batch_id bigint not null references import_batches(id) on delete cascade,
    file_name text not null,
    file_hash text not null,
    file_size_bytes bigint,
    detected_delimiter text,
    detected_encoding text,
    detected_months text[] not null default '{}',
    created_at timestamptz not null default now(),
    constraint uq_import_files_hash unique (file_hash)
);

create table if not exists subscription_records (
    id bigserial primary key,
    provider_id bigint not null references providers(id),
    import_batch_id bigint not null references import_batches(id),
    import_file_id bigint not null references import_files(id),

    -- Month stored as first day of month. Example: 2026-05-01.
    period date not null,

    -- Original fixed dimensions from ANATEL CSV.
    source_row_hash text not null,
    cnpj varchar(14) not null,
    company_name text not null,
    speed_mbps numeric(12, 6),
    municipality_name text not null,
    state char(2) not null,
    speed_range text,
    technology text not null,
    provider_size text,
    person_type text,
    product_type text,
    municipality_code varchar(7),
    economic_group text,
    access_medium text,

    -- Monthly value from the YYYY-MM columns.
    subscriptions_count bigint not null,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),

    constraint ck_subscription_records_count check (subscriptions_count > 0),
    constraint uq_subscription_records_period_source unique (period, source_row_hash)
);

create index if not exists idx_providers_primary_name
    on providers using btree (primary_name);

create index if not exists idx_provider_aliases_alias_name
    on provider_aliases using btree (alias_name);

create index if not exists idx_import_files_import_batch_id
    on import_files (import_batch_id);

create index if not exists idx_subscription_records_import_batch_id
    on subscription_records (import_batch_id);

create index if not exists idx_subscription_records_import_file_id
    on subscription_records (import_file_id);

create index if not exists idx_subscription_records_provider_period
    on subscription_records (provider_id, period);

create index if not exists idx_subscription_records_period
    on subscription_records (period);

create index if not exists idx_subscription_records_state
    on subscription_records (state);

create index if not exists idx_subscription_records_municipality_code
    on subscription_records (municipality_code);

create index if not exists idx_subscription_records_technology
    on subscription_records (technology);

create index if not exists idx_subscription_records_access_medium
    on subscription_records (access_medium);

create index if not exists idx_subscription_records_provider_state_period
    on subscription_records (provider_id, state, period);

create index if not exists idx_subscription_records_provider_municipality_period
    on subscription_records (provider_id, municipality_code, period);

-- Keep public Data API roles from accessing internal tables directly.
revoke all on table providers from anon, authenticated;
revoke all on table provider_aliases from anon, authenticated;
revoke all on table import_batches from anon, authenticated;
revoke all on table import_files from anon, authenticated;
revoke all on table subscription_records from anon, authenticated;

revoke all on all sequences in schema public from anon, authenticated;

alter table providers enable row level security;
alter table provider_aliases enable row level security;
alter table import_batches enable row level security;
alter table import_files enable row level security;
alter table subscription_records enable row level security;

-- Useful view for dashboard queries by provider and month.
create or replace view provider_monthly_totals
with (security_invoker = true) as
select
    provider_id,
    period,
    sum(subscriptions_count) as subscriptions_count
from subscription_records
group by provider_id, period;

-- Useful view for national monthly totals and market share calculations.
create or replace view national_monthly_totals
with (security_invoker = true) as
select
    period,
    sum(subscriptions_count) as subscriptions_count
from subscription_records
group by period;

-- Useful view for fiber participation by provider and month.
create or replace view provider_monthly_fiber_totals
with (security_invoker = true) as
select
    provider_id,
    period,
    sum(subscriptions_count) as subscriptions_count
from subscription_records
where lower(coalesce(access_medium, '')) = 'fibra'
   or upper(coalesce(technology, '')) in ('FTTH', 'FTTB')
group by provider_id, period;

revoke all on table provider_monthly_totals from anon, authenticated;
revoke all on table national_monthly_totals from anon, authenticated;
revoke all on table provider_monthly_fiber_totals from anon, authenticated;
