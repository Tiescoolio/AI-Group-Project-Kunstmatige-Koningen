CREATE TABLE IF NOT EXISTS sessions (
    buid VARCHAR(255) PRIMARY KEY,
    profile_id VARCHAR(255) NOT NULL,
    FOREIGN KEY(profile_id) REFERENCES profiles(id)
)