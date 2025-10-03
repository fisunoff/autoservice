from fastapi import FastAPI

from endpoints import auth, car, customer, pricelist, workers

app = FastAPI()

app.include_router(auth.auth_router, prefix='/auth')
app.include_router(car.car_router, prefix='/car')
app.include_router(customer.customer_router, prefix='/customer')
app.include_router(pricelist.price_list_router, prefix='/price_list')
app.include_router(workers.workers_router, prefix='/worker')
