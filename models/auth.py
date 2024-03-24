#!/usr/bin/env python3
"""
Auth Class
"""
import bcrypt
from models import storage
from models.user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """Hashes the given password using bcrypt
    """
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hash_password


def _generate_uuid() -> str:
    """Generates a new UUID and returns its string representation
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def register_user(self, email: str, password: str) -> None:
        """Registers a new user into the database
        """
        try:
            storage.find_by(User, email=email)
        except NoResultFound:
            user = User(email=email, hashed_password=_hash_password(password))
            return storage.add(user)
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Checks user's credentials
        """
        try:
            user = storage.find_by(User, email=email)
            return bcrypt.checkpw(
                password.encode("utf-8"),
                user.hashed_password.encode("utf-8"))
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates and returns user's session id
        """
        try:
            user = storage.find_by(User, email=email)
            session_id = _generate_uuid()
            storage.update(user, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Returns user object based on it's session id
        """
        if not session_id:
            return None
        try:
            return storage.find_by(User, session_id=session_id)
        except NoResultFound:
            return None

    def require_auth(self, request):
        """ Checks if user is logged in or not
        """
        paths = {
            "admin": [
                '/refund',
                '/dashboard/overview',
                '/dashboard/orders',
                '/orders',
                '/products'],
            "users": [
                '/profile',
                '/user_orders']}
        session_id = request.cookies.get('session_id')
        if not session_id:
            if request.path in paths['admin'] or request.path in paths['users']:
                return True

    def update_password(self, user, new_password: str) -> None:
        """Updates user's password
        """
        try:
            hash_password = _hash_password(new_password)
            return storage.update(user, hashed_password=hash_password)
        except NoResultFound:
            raise ValueError

    def destroy_session(self, user) -> None:
        """Destroys user's session
        """
        storage.update(user, session_id=None)
        return None
