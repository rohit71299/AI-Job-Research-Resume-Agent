
from app.db.base import Base
from app.db.session import engine
from app.models.job_listing import JobListing  # Registers the model

def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    create_tables()
