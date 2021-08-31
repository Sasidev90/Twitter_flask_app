import os
import tweepy
from datetime import datetime
import datetime
from logger import trace, exc

def create_tweepy_client():
    CONSUMER_KEY = 'Q2Gcoh2nNHz14blH9DVk2UlZe'
    CONSUMER_SECRET = 'u9W5KiddAlf7PRPMGHWuHAZfkKaDgY6EMXesDmnwAJMflDD5fg'
    ACCESS_KEY = '1428308621889130497-Nwvgn5ZunUdULBpAa1SG0sl6sc7rX3'
    ACCESS_SECRET = 'FJD00vx9yVu61ar5z27DOnLU7EhLAkvNuTDV8DZZH27cc'
    try:
        trace.info('Initiated for client connection...')
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        client = tweepy.API(auth)
        return client
    except Exception as e:
        exc.exception("Error in create_tweepy_client: ",e)
        print("Error in create_tweepy_client: ",e)


def get_timeline(client, screen_name, last_pulled_at=None):
    try:
        trace.info('Initiated for timeline status')
        timeline = []
        FMT = '%H:%M:%S'
        for status in tweepy.Cursor(client.user_timeline, id=screen_name).items():
            # diff = datetime.strptime(str(last_pulled_at.time()), FMT) - datetime.strptime(str(status.created_at.time()),
            #                                                                               FMT)
            # diff = datetime.strptime('5:31:50', FMT)
            time_change = datetime.timedelta(hours=5, minutes=30, seconds=50)
            status.created_at = status.created_at + time_change
            if last_pulled_at and status.created_at < last_pulled_at:
                break

            timeline.append({
                "id": status.id,
                "tweet": status.text,
                "created_at": status.created_at
            })
        return timeline, len(timeline)
    except Exception as e:
        exc.exception("Error in get_timeline: ",e)
        print("Error in get_timeline: ",e)


def get_timeline_for_user(screen_name, last_pulled_at=None):
    try:
        trace.info('Initiated for get_timeline_for_user...')
        client = create_tweepy_client()
        timeline = get_timeline(client, screen_name, last_pulled_at)
        return timeline
    except Exception as e:
        exc.exception("Error in get_timeline_for_user: ",e)
        print("Error in get_timeline_for_user: ",e)

