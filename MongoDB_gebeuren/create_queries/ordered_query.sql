CREATE TABLE IF NOT EXISTS ordered (
    id INT NOT NULL,
    profile_id INT NOT NULL,
    FOREIGN KEY(profile_id) REFERENCES profiles(id)
)