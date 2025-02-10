from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from dotenv import load_dotenv, dotenv_values 
import os
from sqlmodel import select
from app.db.models import User
from app.crud.user import get_user, get_project_role
load_dotenv()
SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Model for Token with the access_token and the type of the token
class Token(BaseModel):
    access_token: str
    token_type: str

# TokenData Model with username as string
class TokenData(BaseModel):
    email: str | None = None

router = APIRouter(prefix="/security", tags=["Security"])

# Model for the en- and decryption with CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Schema for the OAuth2 System
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/security/token")

# Method to verify if a password and a hashed_password are the same, auto hashes the plain password using pwd_context 
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# checks if the user exists and is authenticated
def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

# Method to create the JWT access token (json web tokens)
# jwt tokens get saved in the browser storage to authenticate the user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Method decodes the jwt token using the shared security key
# returns the user object from the authenticated user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # unauthorized access
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # gets the user name from the token
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    # Retrieve user from the db using the username
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def is_admin(user: User = Depends(get_current_user)):
    if user.is_admin != True:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

def is_product_owner(project_id: int, user: User = Depends(get_current_user)):
    project_role = get_project_role(user.id, project_id)  # Retrieve project role
    print(f"projectrole {project_role}")
    if project_role != 1:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    # checks the hashed passwords and the email with the db
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Set access token expiration time
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Create a new access token with user's email as the subject (sub)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.archived:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Return the currently authenticated user's object
@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

@router.get("/users/check/admin")
async def read_own_items(
    current_user: Annotated[User, Depends(is_admin)],
):
    return [{"admin_state": current_user.is_admin, "user": current_user.email}]

@router.get("/users/check/product_owner")
async def read_own_items(
    current_user: Annotated[User, Depends(is_product_owner)],
):
    return [{"product_owner_state": True, "user": current_user.email}]
