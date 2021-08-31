# TwitterFlask
 
## App to fetch, search, filter tweets from twitter

Built using
- flask
- mysql
- sqlalchemy

## Create app and generate keys & token in twitter developer page
```bash
Create twitter account using : https://twitter.com/i/flow/signup
After create app in twitter developer page: https://developer.twitter.com/en/apply-for-access
In developer page:
* Generate keys and access token
* Enable 3-legged OAuth in Authentication settings, do the following:
    . Update CALLBACK URLS with your flask running port, eg: http://127.0.0.1:8000/login/twitter/authorized
    . Update wesite url https://twitter.com
```
### Set keys and token in app
```bash
After successfully generated keys and token, update the values in config.py and twitter_utils.py (in function 'create_tweepy_client')
```

### Database upadte

```bash
*Import the mysql dump and add the engine credential in db_utils.py and config.py
```

### How to run this app

```bash
git clone https://github.com/Sasidev90/Twitter-Flask.git
```
```bash
cd Twitter-Flask
```
```bash
python app.py
```
Go to ```http://127.0.0.1/```

### Running in docker
```bash
docker-compose up
```

### Working

- Twitter oAuth authentication is done using flask dance, first user is directed to twitter for auth and when the user is authenticated by twitter the user is redirected to the app.
- If the user is visiting the app for the first time, we will fetch all the tweets of user, when the same user is logged into the app next time, all the tweets from his timeline is not fetched only new tweets of the user is fetched from twitter.
- Mysql text search: For searching the tweets of the user I've used keyword search capability of mysql.
