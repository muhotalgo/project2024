from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.dbfactory import db_startup
from app.routes.board import board_router
from app.routes.cart import cart_router
from app.routes.member import member_router
from app.routes.product import product_router

# 서버시작시 디비 생성
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    db_startup()

app = FastAPI(lifespan=lifespan)

# jinja2 설정
templates = Jinja2Templates(directory='views/templates')
app.mount('/static', StaticFiles(directory='views/static'), name='static')

# 외부 라우터 불러오기
app.include_router(product_router, prefix='/shops/product')
app.include_router(cart_router, prefix='/shops')

@app.get("/", response_class=HTMLResponse)
async def index(req: Request):
    return templates.TemplateResponse(
        'index.html', {'request': req})


if __name__ == '_main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)
