from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from endpoints import (
    auth,
    car,
    customer,
    pricelist,
    workers,
    wiki,
    order,
)

app = FastAPI(
    title='Автосервис',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Разрешенные домены
    allow_methods=['*'],  # Разрешенные методы (GET, POST и т. д.)
    allow_headers=['*'],  # Разрешенные заголовки
)

app.include_router(auth.auth_router, prefix='/auth')
app.include_router(car.car_router, prefix='/car')
app.include_router(customer.customer_router, prefix='/customer')
app.include_router(pricelist.price_list_router, prefix='/price_list')
app.include_router(workers.workers_router, prefix='/worker')
app.include_router(wiki.wiki_router, prefix='/wiki')
app.include_router(order.order_router, prefix='/order')
