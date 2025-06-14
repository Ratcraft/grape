import os

DB_PATH = os.environ.get("GRAPE_DATABASE_PATH", "/Users/alexisduchet/Desktop/project/grape/wine.db")
APP_SECRET = os.environ.get("GRAPE_APP_SECRET", "verysecretapikey")