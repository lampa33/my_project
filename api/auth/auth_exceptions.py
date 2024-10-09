from fastapi import HTTPException
from starlette import status


auth_exception = HTTPException(status_code=400, detail="Incorrect username or password")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

token_exception= HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect token type",
    headers={"WWW-Authenticate": "Bearer"},
)

disabled_user_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User is blocked",
    headers={"WWW-Authenticate": "Bearer"},
)