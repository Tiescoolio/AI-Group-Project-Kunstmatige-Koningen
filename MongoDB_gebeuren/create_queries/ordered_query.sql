CREATE TABLE IF NOT EXISTS ordered (
    id VARCHAR(255) NOT NULL,
    profile_id VARCHAR(255) NOT NULL,
    FOREIGN KEY(profile_id) REFERENCES profiles(id)
)