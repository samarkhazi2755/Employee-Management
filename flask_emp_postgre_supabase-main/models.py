import psycopg2


POSTGRES_URL="postgres://postgres.ljtnyzuzegraxqdyshou:2KslYCvZW9rDMdx3@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require"
def get_conn():
    return psycopg2.connect(POSTGRES_URL)
