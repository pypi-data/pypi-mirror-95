import re
from typing import Optional, Tuple

from flask import Request

from fittrackee.responses import (
    ForbiddenErrorResponse,
    HttpResponse,
    UnauthorizedErrorResponse,
)

from .models import User


def is_admin(user_id: int) -> bool:
    """
    Return if user has admin rights
    """
    user = User.query.filter_by(id=user_id).first()
    return user.admin


def is_valid_email(email: str) -> bool:
    """
    Return if email format is valid
    """
    mail_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(mail_pattern, email) is not None


def check_passwords(password: str, password_conf: str) -> str:
    """
    Verify if password and password confirmation are the same and have
    more than 8 characters

    If not, it returns not empty string
    """
    ret = ''
    if password_conf != password:
        ret = 'Password and password confirmation don\'t match.\n'
    if len(password) < 8:
        ret += 'Password: 8 characters required.\n'
    return ret


def register_controls(
    username: str, email: str, password: str, password_conf: str
) -> str:
    """
    Verify if user name, email and passwords are valid

    If not, it returns not empty string
    """
    ret = ''
    if not 2 < len(username) < 13:
        ret += 'Username: 3 to 12 characters required.\n'
    if not is_valid_email(email):
        ret += 'Valid email must be provided.\n'
    ret += check_passwords(password, password_conf)
    return ret


def verify_user(
    current_request: Request, verify_admin: bool
) -> Tuple[Optional[HttpResponse], Optional[int]]:
    """
    Return user id, if the provided token is valid and if user has admin
    rights if 'verify_admin' is True
    """
    default_message = 'Provide a valid auth token.'
    auth_header = current_request.headers.get('Authorization')
    if not auth_header:
        return UnauthorizedErrorResponse(default_message), None
    auth_token = auth_header.split(' ')[1]
    resp = User.decode_auth_token(auth_token)
    if isinstance(resp, str):
        return UnauthorizedErrorResponse(resp), None
    user = User.query.filter_by(id=resp).first()
    if not user:
        return UnauthorizedErrorResponse(default_message), None
    if verify_admin and not is_admin(resp):
        return ForbiddenErrorResponse(), None
    return None, resp


def can_view_workout(
    auth_user_id: int, workout_user_id: int
) -> Optional[HttpResponse]:
    """
    Return error response if user has no right to view workout
    """
    if auth_user_id != workout_user_id:
        return ForbiddenErrorResponse()
    return None
