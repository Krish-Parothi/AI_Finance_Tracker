# dependency
from fastapi import Header, HTTPException
from app.utils.jwt_handler import decode_token

async def auth_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401)
    token = authorization.split(" ")[1]
    payload = decode_token(token)
    return payload["user_id"]