from fastapi import FastAPI

from endpoints import auth, car, customer

app = FastAPI()

app.include_router(auth.auth_router, prefix='/auth')
app.include_router(car.car_router, prefix='/car')
app.include_router(customer.customer_router, prefix='/customer')
