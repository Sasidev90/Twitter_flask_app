import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from logger import trace, exc

engine = create_engine(os.environ.get("DATABASE_URI", "mysql+pymysql://root:admin@localhost:3306/twitter"))

def insert_user(username):
    try:
        trace.info("Initialised insert users in database...")
        query = text("INSERT IGNORE INTO users (username) VALUES (:username)")
        data = {"username": username}
        with engine.connect() as connection:
            connection.execute(query, **data)
    except Exception as e:
        exc.exception(f"Error in insert_user: {e}")
        print(f"Error in insert_user: {e}")


def get_column_for_row(column_name, table_name, filter_column, value):
    try:
        trace.info("Initialised to fetch get_column_for_row from database...")
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT {} FROM {} WHERE {} = '{}'".format(
                    column_name, table_name, filter_column, value
                )))
            row = result.fetchone()
        return row[column_name] if row else None
    except Exception as e:
        exc.exception(f"Error in get_column_for_row: {e}")
        print(f"Error in get_column_for_row: {e}")


def update_last_pulled_time_for_user(username, timestamp):
    try:
        trace.info("Initialised to update_last_pulled_time_for_user in database...")
        data = {"timestamp": timestamp, "username": username}
        query = text("UPDATE users SET last_pulled_at=:timestamp WHERE username = :username")
        with engine.connect() as connection:
            connection.execute(query, **data)
    except Exception as e:
        exc.exception(f"Error in update_last_pulled_time_for_user: {e}")
        print(f"Error in update_last_pulled_time_for_user: {e}")


def write_tweets_to_db(tweets, username):
    try:
        trace.info("Initialised to write_tweets_to_db in database...")
        user_id = get_column_for_row("id", "users", "username", username)
        query = text("INSERT INTO tweets (tweet_id, tweet_text, created_at, twitter_user)"
                     " VALUES (:id, :tweet, :created_at, :twitter_user)")
        with engine.connect() as connection:
            for tweet in tweets:
                tweet.update({"twitter_user": user_id})
                connection.execute(query, **tweet)
    except Exception as e:
        exc.exception(f"Error in write_tweets_to_db: {e}")
        print(f"Error in write_tweets_to_db: {e}")



def initialize_user(username, timestamp):
    try:
        trace.info("Initialised users in database...")
        query = text("INSERT INTO users (username, last_pulled_at) VALUES (:username, :now)")
        data = {"username": username, "now": timestamp}
        with engine.connect() as connection:
            connection.execute(query, **data)
    except Exception as e:
        exc.exception(f"Error in initialize_user: {e}")
        print(f"Error in initialize_user: {e}")


def update_tweets_pulled_for_user(username, count):
    try:
        trace.info("Initialised to update_tweets_pulled_for_user from database...")
        current_tweets_pulled = get_column_for_row("tweets_pulled", "users", "username", username)
        data = {
            "count": current_tweets_pulled + count,
            "username": username,
        }
        query = text("UPDATE users SET tweets_pulled=:count WHERE username = :username")
        with engine.connect() as connection:
            connection.execute(query, **data)
    except Exception as e:
        exc.exception(f"Error in update_tweets_pulled_for_user:  {e}")
        print(f"Error in update_tweets_pulled_for_user:  {e}")


def update_is_completed_status(username, status=True):
    try:
        trace.info("Initialised for update_is_completed_status in database...")
        data = {
            "status": status,
            "username": username,
        }
        query = text("UPDATE users SET is_completed=:status WHERE username = :username")
        with engine.connect() as connection:
            connection.execute(query, **data)
    except Exception as e:
        exc.exception(f"Error in update_is_completed_status: {e}")
        print(f"Error in update_is_completed_status: {e}")


def search_tweets(search_term, username):
    try:
        trace.info("Initialised for serach_tweets from database...")
        if not search_term:
            return []
        user_id = get_column_for_row("id", "users", "username", username)
        results = []
        search_term = ' & '.join(search_term.split())

        query = """
        WITH user_tweets AS (SELECT tweet_text, tweet_tsv, created_at FROM tweets WHERE twitter_user = {})
        SELECT tweet_text, created_at FROM user_tweets
        WHERE tweet_text LIKE %s""".format(user_id)

        value = f'%{search_term}%'
        with engine.connect() as connection:
            rows = connection.execute(query, value)
        for row in rows:
            results.append({
                "tweet": row["tweet_text"],
                "created_at": row["created_at"]
            })
        return results
    except Exception as e:
        exc.exception(f"Error in search_tweets: {e}")
        print(f"Error in search_tweets: {e}")

def get_tweets_of_user(username):
    try:
        trace.info("Initialised to get_tweets_of_user from database...")
        user_id = get_column_for_row("id", "users", "username", username)
        results = []
        query = "SELECT tweet_id, tweet_text, created_at FROM tweets WHERE twitter_user = {}".format(user_id)
        with engine.connect() as connection:
            rows = connection.execute(query)
        for row in rows:
            results.append({
                "id": row["tweet_id"],
                "tweet": row["tweet_text"],
                "created_at": row["created_at"]
            })
        return results
    except Exception as e:
        exc.exception(f"Error in get_tweets_of_user: {e}")
        print(f"Error in get_tweets_of_user: {e}")


def filter_tweets(start_date, end_date, chronological, username):
    try:
        trace.info("Initialised to filter_tweets from database...")
        results = []
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "user_id": get_column_for_row("id", "users", "username", username)
        }
        query = """WITH user_tweets AS (SELECT tweet_text, created_at FROM tweets WHERE twitter_user = :user_id)
        SELECT tweet_text, created_at FROM user_tweets
        WHERE created_at BETWEEN :start_date and DATE_ADD(:end_date,INTERVAL 1 DAY) ORDER BY tweet_text {}
        """.format("ASC" if chronological else "DESC")

        with engine.connect() as connection:
            rows = connection.execute(text(query), data)

        for row in rows:
            results.append({
                "tweet": row["tweet_text"],
                "created_at": row["created_at"]
            })
        return results

    except Exception as e:
        exc.exception(f"Error in filter_tweets: {e}")
        print(f"Error in filter_tweets: {e}")

