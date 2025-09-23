from fastapi import FastAPI

from endpoints import auth

app = FastAPI()

app.include_router(auth.auth_router)
