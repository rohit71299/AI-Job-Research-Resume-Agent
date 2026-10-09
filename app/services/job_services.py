
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.job_listing import JobListing
from app.schemas.job_listing import JobListingCreate

def create_job(db: Session, payload: JobListingCreate) -> JobListing:
    job = JobListing(
        title=payload.title,
        company=payload.company,
        location=payload.location,
        description=payload.description,
        source_url=str(payload.source_url),
    )

    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def list_jobs(db: Session, limit: int = 20, offset: int = 0):
    statement = (
        select(JobListing)
        .order_by(JobListing.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return db.scalars(statement).all()


def get_job(db: Session, job_id: int) -> JobListing | None:
    return db.get(JobListing, job_id)


def delete_job(db: Session, job: JobListing) -> None:
    db.delete(job)
    db.commit()
