CREATE TYPE state AS ENUM('Opened', 'Closed', 'Canceled');
CREATE TYPE res AS ENUM('W', 'L', 'D');

CREATE TABLE users (
	user_id SERIAL PRIMARY KEY,
	name VARCHAR(42) NOT NULL UNIQUE,
	user_password VARCHAR(128) NOT NULL
);

CREATE TABLE sports (
	sport_id SERIAL PRIMARY KEY,
	name VARCHAR(20) NOT NULL UNIQUE,
	description VARCHAR(255)
);

CREATE TABLE events (
	event_id SERIAL PRIMARY KEY,
	admin_id INTEGER REFERENCES users NOT NULL,
	sport_id INTEGER REFERENCES sports NOT NULL,
	event_date TIMESTAMP,
	location VARCHAR(30),
	description VARCHAR(255),
	participants_number_max INTEGER CHECK (participants_number_max > 1),
	status_rating BOOL NOT NULL,
	state_open state NOT NULL
);

CREATE TABLE participants (
	user_id INTEGER REFERENCES users NOT NULL,
	event_id INTEGER REFERENCES events NOT NULL,
	result res,
	UNIQUE (user_id, event_id)
);

CREATE TABLE ratings (
	user_id INTEGER REFERENCES users NOT NULL,
	sport_id INTEGER REFERENCES sports NOT NULL,
	points INTEGER NOT NULL,
	UNIQUE (user_id, sport_id)
);

CREATE TABLE follows (
	user_id INTEGER REFERENCES users NOT NULL,
	sport_id INTEGER REFERENCES sports NOT NULL,
	location VARCHAR(30) NOT NULL,
	radius INTEGER NOT NULL CHECK (radius > 0)
);
