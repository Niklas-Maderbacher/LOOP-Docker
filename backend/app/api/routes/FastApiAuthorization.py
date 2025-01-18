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
    username: str | None = None


# Model for a User, includes username, email and a flag if the account is disabled
class User(BaseModel):
    user_id: int
    username: str
    email: str | None = None
    disabled: bool | None = None
    is_admin: bool

router = APIRouter(prefix="/security", tags=["Security"])

# Model for a User in the Database with the hashed_password of the user
class UserInDB(User):
    hashed_password: str

# Model for the en- and decryption with CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Schema for the OAuth2 System
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/security/token")

fake_users_db = {
    "zoezp": {
        "user_id": 1,
        "username": "zoezp",
        "full_name": "Zoe Zorn-Pauli",
        "email": "zoe.zornpauli@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
        "is_admin": True, 
    },
    "BJ": {
        "user_id": 2,
        "username": "BJ",
        "full_name": "Julian Bierbaum",
        "email": "Julian.Bierbaum@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
        "is_admin": False, 
    }
}

fake_user_project_role_db = {
    "1_1": {  
        "username": "zoezp",
        "role": "product_owner",
        "project_id": 1,
    },
    "2_1": {  
        "username": "BJ",
        "role": "developer",
        "project_id": 1,
    }
}

# gets user from database To-Do
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def get_project_role(db, user_id, project_id):
    key = f"{user_id}_{project_id}"  
    if key in db:  
        return db[key]["role"] 
    else:
        return None

# Method to verify if a password and a hashed_password are the same, auto hashes the plain password using pwd_context 
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# checks if the user exists and is authenticated
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
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
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    # Retrieve user from the db using the username
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def is_admin(user: User = Depends(get_current_user)):
    if user.is_admin != True:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

def is_product_owner(project_id: int, user: User = Depends(get_current_user)):
    project_role = get_project_role(fake_user_project_role_db, user.user_id, project_id)  # Retrieve project role
    if project_role != "product_owner":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    # checks the hashed passwords and the username with the db
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Set access token expiration time
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Create a new access token with user's username as the subject (sub)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Return the currently authenticated user's object
@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

# Return a list of attributes from the current user
@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]

@router.get("/users/check/admin")
async def read_own_items(
    current_user: Annotated[User, Depends(is_admin)],
):
    return [{"admin_state": current_user.is_admin, "user": current_user.username}]

@router.get("/users/check/product_owner")
async def read_own_items(
    current_user: Annotated[User, Depends(is_product_owner)],
):
    return [{"product_owner_state": True, "user": current_user.username}]