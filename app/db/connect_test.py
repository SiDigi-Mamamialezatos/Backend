import psycopg

conn = psycopg.connect(
    "postgresql://postgres.lynvbkbptgsfdsjzzilo:YsqIaKOuyhQvnd8S6RUjOEzAD4c8ysCzniLkJXJdLkL2Y@aws-1-ap-south-1.pooler.supabase.com:5432/postgres?sslmode=require",
    connect_timeout=5,
)

print("✅ Connected!")
conn.close()