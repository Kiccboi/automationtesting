from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from . import api, ui
from .db import init_db
from .services import ApiError

app = FastAPI(title="ShopFlow", version="1.1.0")
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")


@app.on_event("startup")
def startup():
    init_db()


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    body = {"error": {"code": exc.code, "message": exc.message}}
    return JSONResponse(status_code=exc.status, content=body)


app.include_router(api.router)
app.include_router(ui.router)
