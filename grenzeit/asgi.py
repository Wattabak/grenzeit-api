from typing import Union

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from logging import getLogger

logger = getLogger('grenzeit')

app = FastAPI()


@app.get("/")
async def read_root():
    return RedirectResponse(url='/docs', status_code=301)


@app.get("/providers")
async def countries():
    return
