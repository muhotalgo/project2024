from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

visit_router = APIRouter()

templates = Jinja2Templates(directory='views/templates')


@visit_router.get('/visit', response_class=HTMLResponse)
def visit(req: Request):
    return templates.TemplateResponse('visit/visit.html', {'request': req})
