from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.dbfactory import db_startup
from app.routes.faq import faq_router
from app.routes.TOS import TOS_router
from app.routes.board import board_router
from app.routes.cart import cart_router
from app.routes.policy import policy_router
from app.routes.visit import visit_router
from app.routes.member import member_router
from app.routes.product import product_router
from app.routes.qnaboard import myinfo_contacts_router
from app.routes.orders import myinfo_orders_router
from app.services.member import MemberService
from starlette import status


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield # 비동기 처리가 가능하게끔 yield
    db_startup()

app = FastAPI()

# 세션처리를 미들웨어 설정
app.add_middleware(SessionMiddleware, secret_key='02232024duedate')


# jinja2 설정
templates = Jinja2Templates(directory='views/templates')
# app.mount('/static', StaticFiles(directory='views/static'), name='static')

# 외부 route 파일 불러오기
app.include_router(member_router)
app.include_router(faq_router, prefix='/contact')
app.include_router(myinfo_contacts_router)
app.include_router(myinfo_orders_router)
app.include_router(product_router, prefix='/shops/product')
app.include_router(product_router, prefix='/shops/product')
app.include_router(board_router, prefix='/board')
app.include_router(product_router, prefix='/shops')
app.include_router(cart_router, prefix='/shops')
app.include_router(visit_router, prefix='/visit')
app.include_router(policy_router)
app.include_router(TOS_router)

# 서버시작시 디비 생성
@app.on_event('startup')
async def on_startup():
    db_startup()



@app.get("/", response_class=HTMLResponse)
async def index(req: Request):
    return templates.TemplateResponse('index.html',{'request': req})    # 파일명과 넘길 데이터


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)