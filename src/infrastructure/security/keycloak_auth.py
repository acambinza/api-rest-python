import requests
import textwrap
from jose import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://keycloak:8080")
REALM = os.getenv("KEYCLOAK_REALM", "master")
CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "fastapi-client")

# public key
JWKS_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"

security = HTTPBearer()

# Buscar JWKS
jwks = requests.get(JWKS_URL).json()
x5c_b64 = jwks["keys"][0]["x5c"][0]

# Converter para PEM CERTIFICATE correto
pem_key = "-----BEGIN CERTIFICATE-----\n"
pem_key += "\n".join(textwrap.wrap(x5c_b64, 64))
pem_key += "\n-----END CERTIFICATE-----"    


def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, pem_key, algorithms=["RS256"], options={"verify_aud": False})

        if payload.get("azp") != CLIENT_ID :
            raise HTTPException(status_code=401, detail="Invalid Client")

        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

def jwt_auth(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    return verify_jwt(token)
