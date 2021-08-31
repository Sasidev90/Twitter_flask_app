import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', "FJD00vx9yVu61ar5z27DOnLU7EhLAkvNuTDV8DZZH27cc")
    TWITTER_OAUTH_CLIENT_KEY = os.environ.get("API_KEY", "Q2Gcoh2nNHz14blH9DVk2UlZe")
    TWITTER_OAUTH_CLIENT_SECRET = os.environ.get("API_SECRET", "u9W5KiddAlf7PRPMGHWuHAZfkKaDgY6EMXesDmnwAJMflDD5fg")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", 'mysql+pymysql://root:admin@localhost:3306/twitter')



'''
API KEY:    Q2Gcoh2nNHz14blH9DVk2UlZe
API Secret Key:     u9W5KiddAlf7PRPMGHWuHAZfkKaDgY6EMXesDmnwAJMflDD5fg

Access Token:   1428308621889130497-dnRyqIzMDpwHt9x52Y1cmN39dwc9HD
Access Token Secret:    uatfHWQohLvXW63IuqO6XC35LX5YuE6lxdgmYooehMdzl

Access Token:   1428308621889130497-Nwvgn5ZunUdULBpAa1SG0sl6sc7rX3
Access Token Secret:    FJD00vx9yVu61ar5z27DOnLU7EhLAkvNuTDV8DZZH27cc
'''