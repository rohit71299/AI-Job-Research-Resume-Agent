
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.job_listing import JobListingCreate, JobListingResponse
from app.services.job_service import (
    create_job,
    delete_job,
    get_job,
    list_jobs,
)

router = APIRouter(prefix="/api/v1/jobs", tags=["Jobs"])


@router.post(
    "",
    response_model=JobListingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job_endpoint(
    payload: JobListingCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_job(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A job with this source URL already exists.",
        )


@router.get("", response_model=list[JobListingResponse])
def list_jobs_endpoint(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return list_jobs(db, limit=limit, offset=offset)


@router.get("/{job_id}", response_model=JobListingResponse)
def get_job_endpoint(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = get_job(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job listing not found.",
        )

    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_endpoint(
    job_id: int,
    db: Session = Depends(get_db),
):
    job = get_job(db, job_id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job listing not found.",
        )

    delete_job(db, job)
    return None
