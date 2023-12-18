-- Write an SQL Script that creates a table users
-- with the following fields:
-- id(INT), email(VARCHAR), name(VARCHAR), country(ENUM)
CREATE TABLE IF NOT EXISTS users (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255),
	country ENUM("US", "CO", "TN") NOT NULL DEFAULT "US"
	);
