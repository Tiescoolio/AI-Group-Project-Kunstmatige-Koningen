CREATE TABLE IF NOT EXISTS products (
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    name VARCHAR(255),
    brand VARCHAR(100),
    category VARCHAR(100),
    sub_category VARCHAR(100),
    sub_sub_category VARCHAR(100),
    gender VARCHAR(50),
    target_audience VARCHAR(100),
    selling_price  INT,
    mrsp  INT,
    price_discount    INT,
    aanbiedingen  VARCHAR(255),
    recommendable BOOLEAN
)