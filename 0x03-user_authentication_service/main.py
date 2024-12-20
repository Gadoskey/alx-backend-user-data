#!/usr/bin/env python3
"""
Main file
"""
from user import User
import requests

BASE_URL = "http://127.0.0.1:5000"

def register_user(email: str, password: str) -> None:
    """Register a new user."""
    response = requests.post(f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 200, f"Failed to register user. Response: {response.text}"
    assert response.json() == {"email": email, "message": "user created"}
    print("User registration: OK")

def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with the wrong password."""
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 401, f"Expected 401 Unauthorized, got {response.status_code}"
    print("Login with wrong password: OK")

def log_in(email: str, password: str) -> str:
    """Log in with the correct credentials and return the session ID."""
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 200, f"Failed to log in. Response: {response.text}"
    session_id = response.cookies.get("session_id")
    assert session_id, "No session_id found in cookies"
    print("Login: OK")
    return session_id

def profile_unlogged() -> None:
    """Access profile endpoint without logging in."""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, f"Expected 403 Forbidden, got {response.status_code}"
    print("Profile unlogged: OK")

def profile_logged(session_id: str) -> None:
    """Access profile endpoint while logged in."""
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200, f"Failed to access profile. Response: {response.text}"
    print("Profile logged: OK")

def log_out(session_id: str) -> None:
    """Log out the user."""
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200, f"Failed to log out. Response: {response.text}"
    print("Logout: OK")

def reset_password_token(email: str) -> str:
    """Get a reset password token."""
    response = requests.post(f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200, f"Failed to get reset token. Response: {response.text}"
    reset_token = response.json().get("reset_token")
    assert reset_token, "No reset_token found in response"
    print("Reset password token: OK")
    return reset_token

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the password using the reset token."""
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={"email": email, "reset_token": reset_token, "new_password": new_password},
    )
    assert response.status_code == 200, f"Failed to update password. Response: {response.text}"
    assert response.json() == {"email": email, "message": "Password updated"}
    print("Password update: OK")

# Test Sequence
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
