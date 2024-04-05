CREATE TABLE IF NOT EXISTS sessions_products (
    session_buid VARCHAR(255) NOT NULL,
    FOREIGN KEY(session_buid) REFERENCES sessions(buid),
    id VARCHAR(255) NOT NULL
)