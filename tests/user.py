#!/usr/bin/env python3
"""
Test cases for the user view
"""
import requests
import random

EMAIL = f"ahmedrifki.se{random.random()}@gmail.com"
PASSWD = "abc"
NEW_EMAIL = f"ahmedrifki.se{random.random()}@gmail.com"
NEW_PASSWD = "xyz"


def register_user_with_email_not_exists(email: str, password: str) -> None:
    """ Test user's registration endpoint
    """
    url = "http://localhost:5000/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    status_code = response.status_code
    expected_response = {"message": "user created"}
    response = response.json()
    assert response == expected_response
    assert status_code == 201


def register_user_with_email_exists(email: str, password: str) -> None:
    """ Test user's registration endpoint
    """
    url = "http://localhost:5000/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    status_code = response.status_code
    expected_response = {"message": "This email is already registered"}
    response = response.json()
    assert response == expected_response
    assert status_code == 400


def log_in_with_valid_credentials(email: str, password: str) -> str:
    """ Test user login endpoint with valid credentials
    """
    url = "http://localhost:5000/sessions"
    valid_credentials = {"email": email, "password": password}
    response = requests.post(url, data=valid_credentials)
    session_id = response.cookies.get("session_id")
    assert response.status_code == 200
    return session_id


def log_in_with_wrong_password(email: str, password: str) -> None:
    """ Test user login endpoint with invalid credentials
    """
    url = "http://localhost:5000/sessions"
    wrong_credentials = {"email": email, "password": password}
    response = requests.post(url, data=wrong_credentials)
    assert response.status_code == 401


def logged_get_profile(session_id: str) -> None:
    """ Test user's profile endpoint with user logged in
    """
    url = "http://localhost:5000/profile"
    cookie = {"session_id": session_id}
    response = requests.get(url, cookies=cookie)
    assert response.status_code == 200


def unlogged_get_profile() -> None:
    """Test user's profile endpoint with user logged out
    """
    url = "http://localhost:5000/profile"
    response = requests.get(url)
    assert response.status_code == 401


def update_email(session_id: str, email: str) -> str:
    """ Test update user's email endpoint
    """
    url = "http://localhost:5000/profile"
    cookie = {"session_id": session_id}
    email = {"email": email}
    response = requests.put(url, cookies=cookie, data=email).json()
    expected_response = {"message": "Email updated"}
    assert response == expected_response


def update_username(session_id: str, username: str) -> str:
    """ Test update user's username endpoint
    """
    url = "http://localhost:5000/profile"
    cookie = {"session_id": session_id}
    username = {"username": username}
    response = requests.put(url, cookies=cookie, data=username).json()
    expected_response = {"message": "Username updated"}
    assert response == expected_response


def update_password(session_id: str, current_pwd: str, new_pwd: str) -> str:
    """ Test update user's password endpoint
    """
    url = "http://localhost:5000/profile"
    cookie = {"session_id": session_id}
    data = {"currentPassword": current_pwd, "password": new_pwd}
    response = requests.put(url, cookies=cookie, data=data).json()
    expected_response = {"message": "Password updated"}
    assert response == expected_response


def update_password_with_invalid_current_pwd(
        session_id: str, current_pwd: str, new_pwd: str) -> str:
    """ Test update user's password endpoint with invalid current password
    """
    url = "http://localhost:5000/profile"
    cookie = {"session_id": session_id}
    data = {"currentPassword": current_pwd, "password": new_pwd}
    response = requests.put(url, cookies=cookie, data=data)
    assert response.status_code == 401


def log_out(session_id: str) -> None:
    """Test user logout endpoint
    """
    url = "http://localhost:5000/sessions"
    cookie = {"session_id": session_id}
    response = requests.delete(url, cookies=cookie).json()
    assert response == {}


if __name__ == "__main__":
    register_user_with_email_not_exists(EMAIL, PASSWD)
    register_user_with_email_exists(EMAIL, PASSWD)
    session_id = log_in_with_valid_credentials(EMAIL, PASSWD)
    log_in_with_wrong_password(EMAIL, "")
    logged_get_profile(session_id)
    unlogged_get_profile()
    update_email(session_id, NEW_EMAIL)
    update_username(session_id, f"Sseeker{random.random()}")
    update_password(session_id, PASSWD, NEW_PASSWD)
    update_password_with_invalid_current_pwd(session_id, "", NEW_PASSWD)
    log_out(session_id)
