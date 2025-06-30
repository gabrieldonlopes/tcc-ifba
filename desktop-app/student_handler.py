from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from typing import Optional,Union
load_dotenv()

WEB_API_KEY: Optional[str] = os.getenv("WEB_API_KEY")
BASE_URL: Optional[str] = os.getenv("BASE_URL")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

