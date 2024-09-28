from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan():
    pass 


app = FastAPI(lifespan=lifespan)


