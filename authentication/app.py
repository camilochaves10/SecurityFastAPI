from datetime import datetime, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from authentication import schemas
from authentication.authentication import authenticate, create_access_token
from authentication.database import create_all_tables, get_async_session
from authentication.models import AccessToken, User
from authentication.password import get_password_hash




@app.post(
    '/register', status_code = status.HTTP_201_CREATED, response_model = schemas.UserRead
)
async def register(
    user_create: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)
) -> User:
    hashed_password = get_password_hash(user_create.password)
    user = User(*user_create.dict(exclude={'password'}), hashed_password = hashed_password)
    try:
        session.add(user)
        await session.commit()
    except exc.IntegrityError:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, detail='Email already exists'
        )
    return user

@app.post('/token')
async def create_token(
    form_data: OAuth2PasswordRequestForm =
Depends(OAuth2PasswordRequestForm),
session: AsyncSession = Depends(get_async_session),
):
    email: form_data.username
    password: form_data.password
    user = await authenticate(email, password, session)

    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    
    token = await create_access_token(user, session)

    return {'access_token': token.access_token, 'token_type': 'bearer'}

@app.get("/protected-route", response_model=schemas.UserRead)
async def protected_route(user: User = Depends(get_current_user)):
        return user


