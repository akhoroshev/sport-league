CREATE TABLE IF NOT EXISTS users (
	user_id SERIAL PRIMARY KEY,
	name VARCHAR(42) NOT NULL UNIQUE,
	user_password VARCHAR(128) NOT NULL
);

CREATE TABLE IF NOT EXISTS sports (
	sport_id SERIAL PRIMARY KEY,
	name VARCHAR(20) NOT NULL UNIQUE,
	description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS places (
	place_id SERIAL PRIMARY KEY,
	name VARCHAR(42) NOT NULL,
	description VARCHAR(255),
	longitude DECIMAL(9, 6) NOT NULL,
	latitude DECIMAL(9, 6) NOT NULL, 
	UNIQUE (longitude, latitude)
);

CREATE TABLE IF NOT EXISTS events (
	event_id SERIAL PRIMARY KEY,
	admin_id BIGINT UNSIGNED NOT NULL,
	sport_id BIGINT UNSIGNED NOT NULL,
	event_date TIMESTAMP,
	location BIGINT UNSIGNED,
	description VARCHAR(255),
	participants_number_max INTEGER CHECK (participants_number_max > 1),
	status_rating BOOL NOT NULL,
	state_open ENUM('Opened', 'Closed', 'Canceled') NOT NULL,
	FOREIGN KEY(admin_id) REFERENCES users(user_id),
	FOREIGN KEY(sport_id) REFERENCES sports(sport_id),
	FOREIGN KEY(location) REFERENCES places(place_id)
);

CREATE TABLE IF NOT EXISTS participants (
	user_id BIGINT UNSIGNED NOT NULL,
	event_id BIGINT UNSIGNED NOT NULL,
	result ENUM('W', 'L', 'D'),
	UNIQUE (user_id, event_id),
	FOREIGN KEY(user_id) REFERENCES users(user_id),
	FOREIGN KEY(event_id) REFERENCES events(event_id)
);

CREATE TABLE IF NOT EXISTS ratings (
	user_id BIGINT UNSIGNED NOT NULL,
	sport_id BIGINT UNSIGNED NOT NULL,
	points INTEGER NOT NULL,
	UNIQUE (user_id, sport_id),
	FOREIGN KEY(user_id) REFERENCES users(user_id),
	FOREIGN KEY(sport_id) REFERENCES sports(sport_id)
);

CREATE TABLE IF NOT EXISTS follows (
	user_id BIGINT UNSIGNED NOT NULL,
	sport_id BIGINT UNSIGNED NOT NULL,
	location BIGINT UNSIGNED NOT NULL,
	FOREIGN KEY(user_id) REFERENCES users(user_id),
	FOREIGN KEY(sport_id) REFERENCES sports(sport_id),
	FOREIGN KEY(location) REFERENCES places(place_id)
);
