CREATE TABLE IF NOT EXISTS server_config (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT NOT NULL,
    server_name TEXT,
    prod_config BOOLEAN NOT NULL DEFAULT FALSE,
    confession_channel_id BIGINT,
    admin_role_id BIGINT,
    report_channel_id BIGINT,
    confessions_enabled BOOLEAN DEFAULT FALSE,
    message_reacts_enabled BOOLEAN DEFAULT TRUE,
    confession_config JSONB,
    confession_channels JSONB
);

CREATE TABLE IF NOT EXISTS event_logs (
    id SERIAL PRIMARY KEY,
    message_id BIGINT,
    event TEXT,
    created_at TIMESTAMPTZ,
    content TEXT,
    author_id BIGINT,
    mentioned_id BIGINT,
    channel_id BIGINT,
    guild_id BIGINT,
    generated_id TEXT,
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS message_logs (
    id SERIAL PRIMARY KEY,
    message_id BIGINT,
    author_id BIGINT,
    event TEXT,
    created_at TIMESTAMPTZ,
    channel_id BIGINT,
    guild_id BIGINT
);

CREATE TABLE IF NOT EXISTS bubble_tea_entries (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL,
    user_id BIGINT NOT NULL,
    guild_id BIGINT NOT NULL,
    location TEXT,
    description TEXT,
    price NUMERIC,
    currency TEXT,
    image TEXT,
    notes TEXT,
    rating INTEGER
);

CREATE TABLE IF NOT EXISTS tocfl (
    id SERIAL PRIMARY KEY,
    vocab TEXT,
    zhuyin TEXT,
    pinyin TEXT,
    english TEXT,
    level INTEGER,
    part_of_speech TEXT,
    context TEXT
);

CREATE OR REPLACE VIEW total_patted_counts AS
    SELECT mentioned_id AS id, COUNT(*) AS count
    FROM event_logs
    WHERE event = 'pat'
    GROUP BY mentioned_id
    ORDER BY count DESC;

CREATE OR REPLACE VIEW total_patter_counts AS
    SELECT author_id AS id, COUNT(*) AS count
    FROM event_logs
    WHERE event = 'pat'
    GROUP BY author_id
    ORDER BY count DESC;
