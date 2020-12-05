db_path = "sqlite:///base.db"
MIN_PASSWORD_LENGTH = 5


class Config:
    DEBUG = False
    SECRET_KEY = "uZM3KBTnEFXZfCFmzGdgLeYQwRjMD6INp4C0JiO1VHy9LXYsdv"
    SQLALCHEMY_DATABASE_URI = db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
