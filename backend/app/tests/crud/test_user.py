from datetime import datetime
from sqlalchemy.orm import Session

from app.db.models import User
from app.crud.user import get_user, get_all_users, create_user
from app.api.schemas.user import UserCreate 
from app.api.routes.FastApiAuthorization import verify_password

def test_create_user(db: Session):
    user_data = UserCreate(
        email = "user@example.com",
        display_name = "Test User",
        password = "secret",
        microsoft_account = False,
        archived = None,
        last_active = None,
        is_email_verified = False,
        mobile_number = "123456",
        is_admin = False
    )
    
    new_user = create_user(db, user_data)
    assert new_user is not None
    assert new_user.email == user_data.email
    assert new_user.display_name == user_data.display_name
    assert verify_password(user_data.password, new_user.password)

def test_get_user(db: Session):
    user_data = UserCreate(
        email = "user@example.com",
        display_name = "Test User",
        password = "secret",
        microsoft_account = False,
        archived = None,
        last_active = None,
        is_email_verified = False,
        mobile_number = "123456",
        is_admin = False
    )
    
    new_user = create_user(db, user_data)
    user = get_user(db, new_user.email)
    assert user is not None
    assert user == new_user

def test_get_user_not_found(db: Session):
    user = get_user(db, "notfound@example.com")
    assert user is None

def test_get_all_users(db: Session):
    user_data1 = UserCreate(
        email = "user1@example.com",
        display_name = "Test User1",
        password = "secret",
        microsoft_account = False,
        archived = None,
        last_active = None,
        is_email_verified = False,
        mobile_number = "123456",
        is_admin = False
    )
    
    create_user(db, user_data1)

    user_data2 = UserCreate(
        email = "user2@example.com",
        display_name = "Test User2",
        password = "secret",
        microsoft_account = False,
        archived = None,
        last_active = None,
        is_email_verified = False,
        mobile_number = "123456",
        is_admin = False
    )
    
    create_user(db, user_data2)

    users = get_all_users(db)
    assert len(users) > 0