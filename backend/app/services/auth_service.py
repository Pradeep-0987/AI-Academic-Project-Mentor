from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories import user_repository


class DuplicateEmailError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


def register(db: Session, name: str, email: str, password: str):
    normalized_email = email.lower()
    if user_repository.get_by_email(db, normalized_email):
        raise DuplicateEmailError
    try:
        user = user_repository.create_user(db, name, normalized_email, hash_password(password))
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateEmailError from exc
    return user, create_access_token(user.id)


def login(db: Session, email: str, password: str):
    user = user_repository.get_by_email(db, email.lower())
    if user is None or not verify_password(password, user.password_hash):
        raise InvalidCredentialsError
    return user, create_access_token(user.id)
