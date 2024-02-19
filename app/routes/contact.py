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


@qna_router.get('/notice', response_class=HTMLResponse)
def notice(req: Request):
    return templates.TemplateResponse('contact/notice.html', {'request': req})

@qna_router.get('/faq', response_class=HTMLResponse)
def notice(req: Request):
    return templates.TemplateResponse('contact/faq.html', {'request': req})

# @board_router.get('/list/{cpg}', response_class=HTMLResponse)
# def list(req: Request, cpg: int):
#     stpg = int((cpg - 1) / 10) * 10 + 1 # 페이지네이션 시작값
#     bdlist, cnt = BoardService.select_board(cpg)
#     allpage = ceil(cnt /25)  # 총페이지수
#     return templates.TemplateResponse(
#         'board/list.html', {'request': req, 'bdlist': bdlist,
#                             'cpg':cpg, 'stpg':stpg, 'allpage': allpage, 'baseurl': '/board/list/'})

