import contextlib
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, Form, HTTPException, Response, status

TOKEN_COOKIE_NAME = "token"
CSRF_TOKEN_SECRET = "__CHANGE_THIS_WITH_YOUR_OWN_SECRET_VALUE__"

app = FastAPI(lifespan=lifespan)

@app.post('/login')
async def login(
    response: Response,
    email: str= Form(...),
    password: str= Form(...),
    session: AsyncSession = Depends(get_async_session),

) :
    user = await authenticate(email, password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = await create_access_token(user, session)

    response.set_cookie(
        TOKEN_COOKIE_NAME,
        token.access_token,
        max_age=token.max_age(),
        secure=True,
        httponly=True,
        samesite="lax",
    )