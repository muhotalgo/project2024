from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

qna_router = APIRouter()

# jinja2 설정
templates = Jinja2Templates(directory='views/templates')
qna_router.mount('/static', StaticFiles(directory='views/static'), name='static')


@qna_router.get('/qna', response_class=HTMLResponse)
def qna(req: Request):
    return templates.TemplateResponse('contact/qna.html', {'request': req})

@qna_router.get('/faq', response_class=HTMLResponse)
def faq(req: Request):
    return templates.TemplateResponse('contact/faq.html', {'request': req})


@qna_router.get('/notice_list', response_class=HTMLResponse)
def notice_list(req: Request):
    return templates.TemplateResponse('contact/notice_list.html', {'request': req})


@qna_router.get('/notice', response_class=HTMLResponse)
def notice_view(req: Request):
    return templates.TemplateResponse('contact/notice_view.html', {'request': req})


