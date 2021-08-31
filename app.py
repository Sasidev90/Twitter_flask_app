from config import Config
from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from datetime import datetime
from logger import trace, exc
from db_utils import (
    insert_user,
    search_tweets,
    get_tweets_of_user,
    get_column_for_row,
    filter_tweets,
    update_last_pulled_time_for_user,
    initialize_user,
    update_tweets_pulled_for_user,
    write_tweets_to_db,
    update_is_completed_status
)
from forms import FilterForm, SearchForm
from twitter_utils import get_timeline_for_user


class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


app = Flask(__name__, template_folder='./templates')
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.config.from_object(Config)
twitter_bp = make_twitter_blueprint()
app.register_blueprint(twitter_bp, url_prefix="/login")
OAUTHLIB_INSECURE_TRANSPORT = True


@app.route("/", methods=['GET', 'POST'])
def login():
    try:
        if not twitter.authorized:
            trace.info("Initialised for twitter login...")
            return redirect(url_for("twitter.login"))
        resp = twitter.get("account/verify_credentials.json")
        trace.info("Twitter account verified...")
        assert resp.ok
        twitter_username = resp.json()["screen_name"]
        ins = insert_user(twitter_username)
        pull = pull_tweets_of_user(twitter_username)
        form = SearchForm()
        if form.validate_on_submit():
            search_terms = form.search.data
            tweets = search_tweets(search_terms, twitter_username)
        else:
            tweets = get_tweets_of_user(twitter_username)

        context = {
            "username": twitter_username,
            "tweets_pulled": get_column_for_row("tweets_pulled", "users", "username", twitter_username),
            "last_updated_at": get_column_for_row("last_pulled_at", "users", "username", twitter_username)
        }
        return render_template('index.html', context=context, form=form, tweets=tweets)
    except Exception as e:
        exc.exception(f"Error in login: {e}")
        print(f"Error in login: {e}")


@app.route("/filter", methods=['GET', 'POST'])
def filter():
    try:
        trace.info("Initialised for filter option...")
        if not twitter.authorized:
            trace.info("Initialised for twitter login...")
            return redirect(url_for("twitter.login"))
        resp = twitter.get("account/verify_credentials.json")
        assert resp.ok
        twitter_username = resp.json()["screen_name"]

        form = FilterForm()
        if form.validate_on_submit():
            start_date = form.startdate.data
            end_date = form.enddate.data
            chronological = form.chronological.data
            tweets = filter_tweets(
                start_date, end_date, chronological, twitter_username
            )
        else:
            tweets = get_tweets_of_user(twitter_username)

        context = {
            "username": twitter_username
        }
        return render_template('filter.html', context=context, form=form, tweets=tweets)
    except Exception as e:
        exc.exception(f"Error in filter: {e}")
        print(f"Error in filter: {e}")

def pull_tweets_of_user(username):
    try:
        trace.info("Initialised for pull_tweets_of_user...")
        user_id = get_column_for_row("id", "users", "username", username)
        last_pulled_at = get_column_for_row("last_pulled_at", "users", "username", username)
        if user_id:
            update_last_pulled_time_for_user(username, datetime.now())
        else:
            initialize_user(username, datetime.now())

        timeline, count = get_timeline_for_user(username, last_pulled_at)
        write_tweets_to_db(timeline, username)
        update_tweets_pulled_for_user(username, count)
        update_is_completed_status(username)
        return True
    except Exception as e:
        exc.exception(f"Error in pull_tweets_of_user: {e}")
        print(f"Error in pull_tweets_of_user: {e}")

def pull_new_tweets_of_users():
    try:
        trace.info("Initialised for pull_new_tweets_of_users...")
        users = []
        for user in users:
            pull = pull_tweets_of_user(user)
        return True
    except Exception as e:
        exc.exception(f"Error in pull_new_tweets_of_users: {e}")
        print(f"Error in pull_new_tweets_of_users: {e}")


# @app.route("/check")
# def check():
#     return "check"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
