from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

FAQ_router = APIRouter()

templates = Jinja2Templates(directory='views/templates')


@FAQ_router.get('/vi'
                '', response_class=HTMLResponse)
def visit(req: Request):
    return templates.TemplateResponse('FAQ.html', {'request': req})
