from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPBearer
from jose import jwt 
import requests
import os 

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://keycloak:8080")
REALM = os.getenv("KEYCLOAK_REALM", "master")
CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "fastapi-client")

JWKS_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"

security = HTTPBearer

# Buscar chave publica

jwks = requests.get(JWKS_URL).json()
public_key = jwks["keys"][0]["x5x"][0]


def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, public_key, algorithms=["RS256"], audience=CLIENT_ID)
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Token")


async def jwt_auth(credentials=Security(security)):
    token = await credentials.credentials
    return verify_jwt(token)
