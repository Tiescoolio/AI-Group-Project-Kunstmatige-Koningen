CREATE TABLE IF NOT EXISTS sessions_producten (
    session_id VARCHAR(255) NOT NULL,
    FOREIGN KEY(session_id) REFERENCES sessions(id),
    id VARCHAR(255) NOT NULL
)