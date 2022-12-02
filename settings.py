from envparse import Env

env = Env()

POSTGRES_DATABASE_URL = env.str("POSTGRES_DATABASE_URL")
ELASTIC_URL = env.str("ELASTIC_URL")
