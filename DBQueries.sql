
Drop table task_buddy_users;

CREATE TABLE task_buddy_users (
    id INTEGER PRIMARY KEY,
    enc_id TEXT,

    role INTEGER NOT NULL DEFAULT 0,

    is_active INTEGER NOT NULL DEFAULT 1,
    is_staff INTEGER NOT NULL DEFAULT 0,

    user_name TEXT,
    email TEXT NOT NULL UNIQUE,
    email_verify INTEGER NOT NULL DEFAULT 0,

    mobile_number TEXT,
    mobile_verify INTEGER NOT NULL DEFAULT 0,

    mobile_number_2 TEXT,

    password TEXT NOT NULL,

    about TEXT,
    dob DATE,

    gender TEXT CHECK (gender IN ('male','female','other')),

    address_1 TEXT,
    address_2 TEXT,
    address_3 TEXT,

    pincode TEXT,
    isd_code TEXT,
    location_id TEXT,

    longitude NUMERIC,
    latitude NUMERIC,

    auto_city TEXT,
    auto_state TEXT,
    auto_country TEXT,
    auto_ip TEXT,

    profile_pic TEXT,
    identity_proof_type TEXT,
    identity_proof_doc TEXT,

    google_status INTEGER NOT NULL DEFAULT 0,
    google_id TEXT,

    device_type TEXT CHECK (device_type IN ('android','ios','web')),

    website_url TEXT,
    referal_code TEXT,

    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TRIGGER update_task_buddy_users_timestamp
AFTER UPDATE ON task_buddy_users
FOR EACH ROW
BEGIN
    UPDATE task_buddy_users
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = OLD.id;
END;

select * from task_buddy_users;



# # # # # # BElow are new DB tables for the ideation only


-- ===================================================================
-- Service providers (companies)
-- ===================================================================
CREATE TABLE service_providers (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- owner account (role=provider)
    name VARCHAR(255) NOT NULL,
    description TEXT,
    contact_email VARCHAR(254),
    contact_phone VARCHAR(30),
    website VARCHAR(200),
    address_id BIGINT NULL, -- optional FK to addresses (created below)
    active BOOLEAN NOT NULL DEFAULT TRUE,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_service_providers_user ON service_providers (user_id);
CREATE INDEX idx_service_providers_name ON service_providers (name);

-- ===================================================================
-- Addresses (reusable)
-- ===================================================================
CREATE TABLE addresses (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    label VARCHAR(50),                -- e.g. 'home', 'work'
    line_1 VARCHAR(255) NOT NULL,
    line_2 VARCHAR(255),
    line_3 VARCHAR(255),
    city VARCHAR(150),
    state VARCHAR(150),
    country VARCHAR(150),
    pincode VARCHAR(20),
    longitude NUMERIC(10,7),
    latitude NUMERIC(10,7),
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_addresses_user_default ON addresses (user_id, is_default);
CREATE INDEX idx_addresses_city_state ON addresses (city, state);

-- Add FK from provider to address (deferred to avoid cycle if required)
ALTER TABLE service_providers
    ADD CONSTRAINT fk_service_providers_address FOREIGN KEY (address_id)
    REFERENCES addresses(id) ON DELETE SET NULL;

-- ===================================================================
-- Service persons (workers)
-- ===================================================================
CREATE TABLE service_persons (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- user.role must be service_person
    provider_id BIGINT NULL REFERENCES service_providers(id) ON DELETE SET NULL,
    job_title VARCHAR(120),
    skills JSONB NOT NULL DEFAULT '[]'::jsonb,     -- array of skill tags
    phone VARCHAR(30),
    license_number VARCHAR(128),
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    rating NUMERIC(3,2),
    status VARCHAR(30) NOT NULL DEFAULT 'active',  -- active/suspended/inactive
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_service_persons_provider ON service_persons (provider_id);
CREATE INDEX idx_service_persons_available_status ON service_persons (is_available, status);
CREATE INDEX idx_service_persons_user ON service_persons (user_id);
CREATE INDEX idx_service_persons_skills_gin ON service_persons USING GIN (skills);

-- ===================================================================
-- Consumers (customers)
-- ===================================================================
CREATE TABLE consumers (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- user.role must be consumer
    phone VARCHAR(30),
    default_address_id BIGINT NULL REFERENCES addresses(id) ON DELETE SET NULL,
    preferences JSONB NOT NULL DEFAULT '{}'::jsonb,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_consumers_user ON consumers (user_id);
CREATE INDEX idx_consumers_phone ON consumers (phone);
CREATE INDEX idx_consumers_preferences_gin ON consumers USING GIN (preferences);

-- ===================================================================
-- Devices
-- ===================================================================
CREATE TABLE devices (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    device_type VARCHAR(20) NOT NULL, -- android / ios / web
    device_id VARCHAR(255),           -- push token or device identifier
    last_seen TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_devices_user_type ON devices (user_id, device_type);

-- ===================================================================
-- Service categories & services (catalog)
-- ===================================================================
CREATE TABLE service_categories (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    slug VARCHAR(150) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE services (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255),
    category_id BIGINT NULL REFERENCES service_categories(id) ON DELETE SET NULL,
    description TEXT,
    base_price NUMERIC(10,2),
    duration_minutes INT,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_services_title ON services (title);
CREATE INDEX idx_services_active ON services (active);
CREATE INDEX idx_services_metadata_gin ON services USING GIN (metadata);

-- provider <> service many-to-many table
CREATE TABLE provider_services (
    provider_id BIGINT NOT NULL REFERENCES service_providers(id) ON DELETE CASCADE,
    service_id BIGINT NOT NULL REFERENCES services(id) ON DELETE CASCADE,
    PRIMARY KEY (provider_id, service_id)
);

CREATE INDEX idx_provider_services_provider ON provider_services (provider_id);
CREATE INDEX idx_provider_services_service ON provider_services (service_id);

-- ===================================================================
-- Provider admins (many-to-many: provider <-> user)
--   - holds additional user accounts allowed to administer a provider.
--   - We cannot enforce user.role in SQL easily; enforce in application logic or via triggers.
-- ===================================================================
CREATE TABLE provider_admins (
    provider_id BIGINT NOT NULL REFERENCES service_providers(id) ON DELETE CASCADE,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_at_provider VARCHAR(100) DEFAULT NULL, -- optional: e.g., 'manager', 'billing'
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (provider_id, user_id)
);

CREATE INDEX idx_provider_admins_user ON provider_admins (user_id);
CREATE INDEX idx_provider_admins_provider ON provider_admins (provider_id);

-- ===================================================================
-- Bookings (appointments / work orders)
-- ===================================================================
CREATE TABLE bookings (
    id BIGSERIAL PRIMARY KEY,
    consumer_id BIGINT NOT NULL REFERENCES consumers(id) ON DELETE CASCADE,
    service_id BIGINT NULL REFERENCES services(id) ON DELETE SET NULL,
    provider_id BIGINT NULL REFERENCES service_providers(id) ON DELETE SET NULL,
    service_person_id BIGINT NULL REFERENCES service_persons(id) ON DELETE SET NULL,
    scheduled_at TIMESTAMPTZ NOT NULL,
    duration_minutes INT,
    price NUMERIC(12,2),
    status VARCHAR(30) NOT NULL DEFAULT 'pending', -- pending, accepted, in_progress, completed, cancelled
    address_id BIGINT NULL REFERENCES addresses(id) ON DELETE SET NULL,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_bookings_consumer ON bookings (consumer_id);
CREATE INDEX idx_bookings_provider ON bookings (provider_id);
CREATE INDEX idx_bookings_service_person ON bookings (service_person_id);
CREATE INDEX idx_bookings_status ON bookings (status);
CREATE INDEX idx_bookings_scheduled ON bookings (scheduled_at);

-- ===================================================================
-- Helpful GIN indexes for JSONB fields used frequently
-- ===================================================================
CREATE INDEX idx_service_providers_metadata_gin ON service_providers USING GIN (metadata);
CREATE INDEX idx_service_persons_metadata_gin ON service_persons USING GIN (metadata);
CREATE INDEX idx_consumers_metadata_gin ON consumers USING GIN (metadata);

-- ===================================================================
-- Optional: triggers to update updated_at timestamp on update
-- (If you prefer DB-level updated_at maintenance)
-- ===================================================================
CREATE OR REPLACE FUNCTION trigger_set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

-- Attach trigger to tables that have updated_at
CREATE TRIGGER trg_service_providers_updated_at
BEFORE UPDATE ON service_providers
FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

CREATE TRIGGER trg_service_persons_updated_at
BEFORE UPDATE ON service_persons
FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

CREATE TRIGGER trg_consumers_updated_at
BEFORE UPDATE ON consumers
FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

CREATE TRIGGER trg_bookings_updated_at
BEFORE UPDATE ON bookings
FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at();

-- ===================================================================
-- Notes / recommendations
-- ===================================================================
-- 1) Role enforcement:
--    The FK constraints point to users.id but do not enforce the user's .role value.
--    Enforce role constraints (e.g., user.role='provider' for service_providers.user_id)
--    in application logic or add database triggers to check users.role if you need DB-level enforcement.
--
-- 2) Geo queries:
--    For production-scale geographic queries, consider installing PostGIS and using geometry/geography columns
--    with spatial indexes instead of numeric lon/lat and Haversine math.
--
-- 3) Files / media:
--    profile_pic and identity_proof fields in Django map to string paths in DB; here we store just references (addresses/metadata).
--
-- 4) Soft delete:
--    Prefer using boolean `active` / `is_active` flags rather than hard deletes to preserve historical bookings.
--
-- 5) Indexes:
--    Add additional indexes (or partial indexes) based on query patterns discovered in production.

