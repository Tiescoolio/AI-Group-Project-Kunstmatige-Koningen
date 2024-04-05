CREATE TABLE IF NOT EXISTS sessions (
    id VARCHAR(255) NOT NULL,
    has_sale BOOLEAN,
    profile_id VARCHAR(255) NOT NULL,
    FOREIGN KEY(profile_id) REFERENCES profiles(id)
)