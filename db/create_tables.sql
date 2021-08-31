-- users Table Definition ----------------------------------------------
CREATE DATABASE IF NOT EXISTS twitter;
use twitter;

CREATE TABLE IF NOT EXISTS users(
	id INT NOT NULL,
  	username VARCHAR(20),
  	job_id INT NOT NULL,
  	is_completed INT NOT NULL,
  	tweets_pulled INT NOT NULL,
  	last_pulled_at VARCHAR(75),
  	PRIMARY KEY(id)
);


-- tweets Table Definition ----------------------------------------------

CREATE TABLE IF NOT EXISTS tweets (
    tweet_id INT NOT NULL,
    tweet_text TEXT,
    tweet_tsv TEXT,
    created_at VARCHAR(75),
    twitter_user INT REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY(tweet_id)
);
