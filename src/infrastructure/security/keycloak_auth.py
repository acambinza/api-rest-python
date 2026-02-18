import requests
import textwrap
from jose import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://keycloak:8080")
REALM = os.getenv("KEYCLOAK_REALM", "master")
CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "fastapi-client")

JWKS_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"

security = HTTPBearer()

# Buscar JWKS
jwks = requests.get(JWKS_URL).json()
x5c_b64 = jwks["keys"][0]["x5c"][0]

# Converter para PEM correto
pem_key = "-----BEGIN PUBLIC KEY-----\n"
pem_key += "\n".join(textwrap.wrap(x5c_b64, 64))  # quebra de linha a cada 64 chars
pem_key += "\n-----END PUBLIC KEY-----"

def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, pem_key, algorithms=["RS256"], audience=CLIENT_ID)
        return payload
    except Exception as e:
        print(f"JWT verification error: {e}")
        raise HTTPException(status_code=401, detail="Invalid Token")

def jwt_auth(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    print(f"Recebido token: {token}")
    return verify_jwt(token)
