"""
Simple script to initialize the database.
Run this after setting up your Postgres database.
"""
from database import engine, Base

if __name__ == "__main__":
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


