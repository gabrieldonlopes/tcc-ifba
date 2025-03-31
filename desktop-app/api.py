import requests as req 
import os 

from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
WEB_API_KEY = os.getenv("WEB_API_KEY")

url = "http://localhost:8000/data"
headers = {
    "api-key":WEB_API_KEY,
    "Content-Type": "application/json"  
}

class User(BaseModel):
    name: str
    password: str

new_user = User(name="foo",password="password123")

response = req.post(url=url,headers=headers,json=new_user.model_dump(),verify=False)

print(response.status_code)
print(response.text)