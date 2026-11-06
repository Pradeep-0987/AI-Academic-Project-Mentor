from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.repositories import student_repository
from app.schemas.student import (
    ProfilePayload,
    SkillsAssessmentPayload,
    StudentFullDataResponse,
)

router = APIRouter(prefix="/api/students", tags=["students"])


@router.post("/profile", status_code=status.HTTP_200_OK)
def save_profile(
    data: ProfilePayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = student_repository.upsert_profile(
        db=db,
        user_id=current_user.id,
        institution=data.institution,
        department=data.department,
        semester=data.semester,
        graduation_year=data.graduation_year,
    )
    return {"status": "ok", "profile_id": str(profile.id)}


@router.post("/skills", status_code=status.HTTP_200_OK)
def save_skills(
    data: SkillsAssessmentPayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skills_data = [s.model_dump() for s in data.skills]
    saved_skills = student_repository.save_skills(db, current_user.id, skills_data)
    saved_interests = student_repository.save_interests(db, current_user.id, data.interests)
    return {
        "status": "ok",
        "skills_saved": len(saved_skills),
        "interests_saved": len(saved_interests),
    }


@router.get("/me", response_model=StudentFullDataResponse)
def get_student_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = student_repository.get_profile(db, current_user.id)
    skills = student_repository.get_skills(db, current_user.id)
    interests = student_repository.get_interests(db, current_user.id)

    return StudentFullDataResponse(
        institution=profile.institution if profile else None,
        department=profile.department if profile else None,
        semester=profile.semester if profile else None,
        graduation_year=profile.graduation_year if profile else None,
        onboarding_completed=profile.onboarding_completed if profile else False,
        skills=[
            {
                "name": s.skill_name,
                "level": s.proficiency_level,
                "isCustom": s.is_custom,
            }
            for s in skills
        ],
        interests=[i.interest_name for i in interests],
    )
