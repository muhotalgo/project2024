from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

TOS_router = APIRouter()

templates = Jinja2Templates(directory='views/templates')


@TOS_router.get('/TOS', response_class=HTMLResponse)
def visit(req: Request):
    return templates.TemplateResponse('TOS.html', {'request': req})
