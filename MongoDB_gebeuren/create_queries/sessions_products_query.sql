CREATE TABLE IF NOT EXISTS sessions_products (
    session_id VARCHAR(255) NOT NULL,
    FOREIGN KEY(session_id) REFERENCES session_id(id),
    id VARCHAR(255) NOT NULL
)