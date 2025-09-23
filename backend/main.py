from fastapi import FastAPI

from endpoints import auth, car

app = FastAPI()

app.include_router(auth.auth_router, prefix='/auth')
app.include_router(car.car_router, prefix='/car')
