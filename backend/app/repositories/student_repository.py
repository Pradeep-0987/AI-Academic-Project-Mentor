import uuid
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.models.student import StudentProfile, StudentSkill, StudentInterest


def get_profile(db: Session, user_id: uuid.UUID) -> StudentProfile | None:
    return db.scalar(select(StudentProfile).where(StudentProfile.user_id == user_id))


def upsert_profile(
    db: Session,
    user_id: uuid.UUID,
    institution: str,
    department: str,
    semester: str,
    graduation_year: int,
) -> StudentProfile:
    profile = get_profile(db, user_id)
    if profile:
        profile.institution = institution
        profile.department = department
        profile.semester = semester
        profile.graduation_year = graduation_year
        profile.onboarding_completed = True
    else:
        profile = StudentProfile(
            user_id=user_id,
            institution=institution,
            department=department,
            semester=semester,
            graduation_year=graduation_year,
            onboarding_completed=True,
        )
        db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def save_skills(
    db: Session,
    user_id: uuid.UUID,
    skills: list[dict],
) -> list[StudentSkill]:
    # Replace existing skills for this user
    db.execute(delete(StudentSkill).where(StudentSkill.user_id == user_id))
    skill_objs = []
    for s in skills:
        name = s.get("name") or s.get("skill_name") or ""
        level = s.get("level") or s.get("proficiency_level") or "Intermediate"
        if name.strip():
            obj = StudentSkill(
                user_id=user_id,
                skill_name=name.strip(),
                proficiency_level=level.strip(),
                is_custom=bool(s.get("isCustom") or s.get("is_custom")),
            )
            db.add(obj)
            skill_objs.append(obj)
    db.commit()
    return skill_objs


def save_interests(
    db: Session,
    user_id: uuid.UUID,
    interests: list[str],
) -> list[StudentInterest]:
    # Replace existing interests for this user
    db.execute(delete(StudentInterest).where(StudentInterest.user_id == user_id))
    interest_objs = []
    for i in interests:
        if isinstance(i, str) and i.strip():
            obj = StudentInterest(
                user_id=user_id,
                interest_name=i.strip(),
                is_custom=False,
            )
            db.add(obj)
            interest_objs.append(obj)
    db.commit()
    return interest_objs


def get_skills(db: Session, user_id: uuid.UUID) -> list[StudentSkill]:
    return list(db.scalars(select(StudentSkill).where(StudentSkill.user_id == user_id)).all())


def get_interests(db: Session, user_id: uuid.UUID) -> list[StudentInterest]:
    return list(db.scalars(select(StudentInterest).where(StudentInterest.user_id == user_id)).all())
