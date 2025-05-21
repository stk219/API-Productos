class DevelopmentConfig():
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres.turvbictdekpoweirkds:ecommerce*219@aws-0-us-east-2.pooler.supabase.com:6543/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig
}
