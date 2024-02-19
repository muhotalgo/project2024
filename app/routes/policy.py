from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

policy_router = APIRouter()

templates = Jinja2Templates(directory='views/templates')


@policy_router.get('/policy', response_class=HTMLResponse)
def visit(req: Request):
    return templates.TemplateResponse('policy.html', {'request': req})
