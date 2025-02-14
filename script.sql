-- MEMBERS

-- members table
create extension if not exists "uuid-ossp";
-- drop table if exists members;
create table if not exists members (
    id uuid default uuid_generate_v4() primary key,
    first_names text not null check(char_length(trim(first_names)) > 0),
    last_names text not null check(char_length(trim(first_names)) > 0),
    phone_number text unique,
    whatsapp_number text unique,
    email varchar(100) unique not null,
    gender varchar(1) not null, --male or female | M/F
    date_of_birth date not null check(date_of_birth <= current_date - interval '13 years'), -- ensures member must be at
    -- least 13 years old
    address text not null,
    is_baptized boolean not null, --true or false
    is_born_again boolean not null,
    cell_id serial references cells(id) on delete set null,
    fellowship_center_id serial references fellowship_centers(id) on delete set null,
    department_id serial references departments(id) on delete set null,
    foundation_school_status text not null, -- graduated, enrolled, un-enrolled
    joined_on date not null, -- assume first day of first month of specified year if date is not known
    professional_status text, -- employed, unemployed, student
    occupation text,
    school_name text,
    emergency_contact_name text not null, -- could be parent, sibling etc
    emergency_contact_relation text not null, -- mother, father, aunt, uncle, grandmother, grandfather, brother, sister,
        -- friend, neighbour, spouse, other
    emergency_contact_phone text not null,
    emergency_contact_whatsapp text,
    created_on timestamptz not null default (current_timestamp at time zone 'Africa/Douala'), -- date member was created in db
    last_updated timestamptz not null default (current_timestamp at time zone 'Africa/Douala'), -- date any row was updated/modified
    profile_photo bytea not null
);

-- cells table
-- drop table if exists cells;
create table if not exists cells (
  id serial primary key,
  leader_id uuid references members(id) on delete set null, -- references the member ID in members table
  assistant_id uuid references members(id) on delete set null, -- references the member ID in members table
  cell_name text unique not null,
  venue text not null, -- address of the cell
  meeting_day text not null, -- selects between Monday to Sunday
  meeting_time time not null,
  member_count int not null,
  creation_date date not null, -- date cell was birthed
  created_on timestamptz not null default (current_timestamp at time zone 'Africa/Douala'), -- date cell was created in db
  last_updated timestamptz not null default (current_timestamp at time zone 'Africa/Douala'),
  is_senior_cell boolean not null
);

-- departments table
-- drop table if exists departments;
create table if not exists departments (
    id serial primary key,
    leader_id uuid references members(id) on delete set null, -- references id in members table
    assistant_id uuid references members(id) on delete set null, -- references id in members table
    name text unique not null,
    member_count int not null,
    description text,
    created_on timestamptz not null default (current_timestamp at time zone 'Africa/Douala'), -- date department was created in db
    last_updated timestamptz not null default (current_timestamp at time zone 'Africa/Douala')
);

-- fellowship centers table
-- drop table if exists fellowship_centers;
create table if not exists fellowship_centers (
    id serial primary key,
    leader_id uuid references members(id) on delete set null, --references member from members table
    assistant_id uuid references members(id) on delete set null,
    venue text not null, -- address of the center eg Buea Town
    member_count int not null,
    created_on timestamptz not null default (current_timestamp at time zone 'Africa/Douala'), -- date department was created in db
    last_updated timestamptz not null default (current_timestamp at time zone 'Africa/Douala')
);

-- FINANCES

-- ROR
-- drop table if exists rhapsody_of_realities
create table if not exists rhapsody_of_realities (
    id serial primary key,
    member_id uuid references members(id) on delete restrict, -- references member in members table
    amount int not null,
    status text not null, -- given | pledged
    method text not null, -- cash | MTN Momo | Orange Money
    date date not null, -- date amount was given
    created_on timestamptz not null default (current_timestamp at time zone 'Africa/Douala'), -- date partnership was created in db
    last_updated timestamptz not null default (current_timestamp at time zone 'Africa/Douala') -- date partnership was updated (if updated)
);

-- TAP

-- HS

-- L&B
