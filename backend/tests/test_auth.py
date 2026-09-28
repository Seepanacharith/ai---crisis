import pytest
from app.auth.security import hash_password, verify_password, create_access_token

def test_password_hashing():
    pwd = "EmergencyPassword123!"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False

def test_jwt_creation():
    token = create_access_token({"sub": "user_123", "email": "crisis@companion.com"})
    assert isinstance(token, str)
    assert len(token) > 20
