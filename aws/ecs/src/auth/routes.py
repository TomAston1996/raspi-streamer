'''
This file contains the routes for the authentication module. 
The routes are used to authenticate the user and provide a token for accessing the API.
Author: Tom Aston
'''

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter()

@auth_router.post("/token")
def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": form_data.username + 'token', "token_type": "bearer"}


@auth_router.get("/test")
def test_auth(token: str = Depends(oauth2_scheme)):
    return {"token": token}
