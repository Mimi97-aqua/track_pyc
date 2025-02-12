-- MEMBERS

-- members table
create table members (
    id uuid,
    first_name varchar(255),
    last_name varchar(255),
    phone_number varchar(255), --includes country code
    email varchar(255),
    gender varchar(20), --male or female
    date_of_birth date,
    address varchar(255),
    is_baptized boolean, --true or false
    is_born_again boolean,
    cell_id int, -- references ID in cells table
    fellowship_center_id int,
    foundation_school_status varchar(255), -- graduated, enrolled, un-enrolled
    department_id int,
    joined_on date, -- assume first day of first month of specified year if date is not known
    professional_status varchar(255), -- employed, unemployed, student
    occupation varchar(255),
    emergency_contact_name varchar(255), -- could be parent, sibling etc
    emergency_contact_relation varchar(255), -- mother, father, aunt, uncle, grandmother, grandfather, brother, sister,
        -- friend, neighbour, spouse, other
    emergency_contact_phone varchar(255),
    emergency_contact_whatsapp varchar(255),
    created_on timestamp, -- date member was created in db
    updated_on timestamp,
    profile_photo bytea,
);

-- cells table
create table cells (
  id int,
  leader_id uuid(), -- references the member ID in members table
  assistant_id uuid(), -- references the member ID in members table
  cell_name varchar(255),
  venue varchar(255), -- address of the cell
  meeting_day varchar(255), -- selects between Monday to Sunday
  meeting_time timestamp,
  member_count int,
  creation_date date, -- date cell was birthed
  created_on timestamp, -- date cell was created in db
  updated_on timestamp,
  is_senior_cell boolean
);

-- departments table
create table departments (
    id int,
    leader_id uuid(), -- references id in members table
    assistant_id uuid(), -- references id in members table
    name varchar(255),
    member_count int,
    description varchar(255),
    created_on timestamp, -- date department was created in db
    updated_on timestamp
);

-- fellowship centers table
create table fellowship_center (
    id int,
    leader_id uuid(), --references member from members table
    assistant_id uuid(),
    venue varchar(255), -- address of the center eg Buea Town
    member_count int
);

-- FINANCES

-- ROR
create table rhapsody_of_realities (
    id int,
    member_id uuid(), -- references member in members table
    amount int,
    status varchar(255), -- given | pledged
    method varchar(255), -- cash | MTN Momo | Orange Money
    date date
);