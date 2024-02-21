from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi import status
from app.schemas.contact import NewContact
from app.services.contact import ContactService
from math import ceil

contact_router = APIRouter()

templates = Jinja2Templates(directory='views/templates')
contact_router.mount('/static', StaticFiles(directory='views/static'), name='static')

# 페이징 알고리즘
# 페이지당 게시글 수 : 25
# 1page : 1 ~ 25
# 2page : 26 ~ 50
# 3page : 51 ~ 75
# ...
# npage : (n-1)*25 ~ (n)*25+25

# 페이지네이션 알고리즘
# 현재 패이지에 따라 보여줄 페이지 블록 결정
# ex) 총 페이지 수 : 27일때
# cpg = 1: 1 2 3 4 5 6 7 8 9 10
# cpg = 3: 1 2 3 4 5 6 7 8 9 10
# cpg = 9: 1 2 3 4 5 6 7 8 9 10
# cpg = 11: 11 12 13 14 15 16 17 18 19 20
# cpg = 17: 11 12 13 14 15 16 17 18 19 20
# cpg = 23: 21 22 23 24 25 26 27 28 29 30

# cpg = n: m m+1 m+2 ... m+9
# m = ((cpg - 1) / 10) * 10 + 1


@contact_router.get('/contact_list/{cpg}', response_class=HTMLResponse)
def list(req: Request, cpg: int):
    stpg = int((cpg - 1) / 10) * 10 + 1     # 페이지네이션 시작값
    cdlist, cnt = ContactService.select_contact(cpg)
    allpage = ceil(cnt /25)     # 총 페이지 수
    return templates.TemplateResponse('contact/list.html',
                                      {'request': req, 'cdlist': cdlist, 'cpg': cpg, 'stpg': stpg, 'allpage': allpage, 'baseurl': '/contact/list/'})

@contact_router.get('/contact_list/{ftype}/{fkey}/{cpg}', response_class=HTMLResponse)
def find(req: Request, ftype: str, fkey: str, cpg: int):
    stpg = int((cpg - 1) / 10) * 10 + 1     # 페이지네이션 시작값
    cdlist, cnt = ContactService.find_select_contact(ftype, '%'+fkey+'%', cpg)
    allpage = ceil(cnt /25)     # 총 페이지 수
    return templates.TemplateResponse(
        'contact/list.html',{'request': req, 'cdlist': cdlist,
                           'cpg': cpg, 'stpg': stpg, 'allpage': allpage, 'baseurl': f'/contact/list/{ftype}/{fkey}/'})


@contact_router.get('/notice_write',  response_class=HTMLResponse)
def write(req: Request):
    return templates.TemplateResponse('contact/write.html', {'request': req})


@contact_router.post('/notice_write')
def writeok(cdto: NewContact):
    res_url = '/captcha_error'
    if ContactService.check_captcha(cdto):    # captcha 체크가 true 라면
        result = ContactService.insert_board(cdto)
        res_url = '/write_error'
        if result.rowcount > 0: res_url = '/contact/list/1'

    return RedirectResponse(res_url, status_code=status.HTTP_302_FOUND)


@contact_router.get('/view/{cno}', response_class=HTMLResponse)
def view(req: Request, cno: str):

    cd=ContactService.selectone_contact(cno)[0]
    ContactService.update_count_contact(cno)
    return templates.TemplateResponse('board/view.html', {'request': req, 'cd': cd})