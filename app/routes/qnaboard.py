from fastapi import APIRouter, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status

from app.services.member import MemberService
from app.services.qnaboard import QnaBoardService
from app.schemas.qnaboard import NewQna

myinfo_contacts_router = APIRouter()

# jinja2 설정
templates = Jinja2Templates(directory='views/templates')
myinfo_contacts_router.mount('/static', StaticFiles(directory='views/static'), name='static')


# 마이페이지 / 내 질문 내역 보기 (list)
# 마이페이지 / 내 질문 내역 / 글쓰기 페이지


@myinfo_contacts_router.get('/myinfo/contacts/write', response_class=HTMLResponse)
def write(req: Request):
    if 'm' not in req.session:
        return RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)

    myinfo = MemberService.selectone_member(req.session['m'])
    return templates.TemplateResponse('myinfo/contacts/write.html',{'request': req, 'my': myinfo})


@myinfo_contacts_router.post('/myinfo/contacts/write')
def writeok(bdto: NewQna):

    res_url = '/error'
    # print(title, userid, contents)
    # print(attach.filename, attach.content_type, attach.size)         # 콘솔에서 정보확인

    if QnaBoardService.check_captcha(bdto):    # captcha 체크가 true 라면 아래진행
        result = QnaBoardService.insert_board(bdto)
        res_url = '/write_error'
        if result.rowcount > 0: res_url = '/myinfo/contacts'


    return RedirectResponse(res_url, status_code=status.HTTP_302_FOUND)







# @myinfo_contacts_router.get('/myinfo/contacts', response_class=HTMLResponse)
# @myinfo_contacts_router.get('/myinfo/contacts/{action}', response_class=HTMLResponse)
# def contacts_and_write(req: Request, action: str = None):
#     if 'm' not in req.session:
#         return RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)
#
#     myinfo = MemberService.selectone_member(req.session['m'])
#
#     if action == 'write':
#         return templates.TemplateResponse('myinfo/contacts/write.html', {'request': req, 'my': myinfo, 'action': action})
#     else:
#         return templates.TemplateResponse('myinfo/contacts/contacts.html', {'request': req, 'my': myinfo, 'action': action})

# qna 글쓰기
# @myinfo_contacts_router.post('/myinfo/contacts/write')
# async def contacts_writeok(title: str = Form(), userid: str = Form(), contents: str = Form(), response: str = Form()):
#
#     # def contacts_writeok(bdto: NewQna):
#     # ramification = HTMLResponse("""
#     # #             <script>
#     # #                 alert('게시글 작성에 실패했습니다.');
#     # #                 window.location.href = '/myinfo';
#     # #             </script>
#     # #         """)
#     # res_url = ramification
#
#     res_url = '/error'
#
#     if QnaBoardService.check_captcha(response):    # captcha 체크가 true 라면 아래진행
#         bdto = NewQna(title=title, userid=userid, contents=contents)
#         res_url = '/write_error'
#         result = QnaBoardService.insert_board(bdto)
#
#         if result.rowcount > 0: res_url = '/myinfo/contact'
#
#     return RedirectResponse(res_url, status_code=status.HTTP_302_FOUND)




# 페이징 알고리즘
# 페이지당 게시글 수 : 25개 지정
# 1 page : 1 ~ 25
# 2 page : 26 ~ 50
# 3 page : 51 ~ 75
# ...
# n page : (n-1)*25+1 ~ 25*n

# 페이지네이션 알고리즘
# 현재페이지에 따라 보여줄 페이지 블록 결정
# ex) 총 페이지수 : 27일
# cpg = 1: 1 2 3 4 5 6 7 8 9 10
# cpg = 3: 1 2 3 4 5 6 7 8 9 10
# cpg = 9: 1 2 3 4 5 6 7 8 9 10
# cpg = 11: 11 12 13 14 15 16 17 18 19 20
# cpg = 17: 11 12 13 14 15 16 17 18 19 20
# cpg = 23: 21 22 23 24 25 26 27
# cpg = n: m m+1 m+2 ... m+9
# 따라서, cpg에 따라 페이지블록의 시작값 계산
# m = ((cpg - 1) / 10) * 10 + 1 // cpg는 정수가 되어야함.

#
# @myinfo_contacts_router.get('/myinfo/contacts', response_class=HTMLResponse)
# def contacts(req: Request):
#
#     return templates.TemplateResponse('myinfo/contacts/contacts.html',{'request': req, 'my': myinfo})
#     uid = myinfo.userid

@myinfo_contacts_router.get('/myinfo/contacts/{cpg}', response_class=HTMLResponse)
@myinfo_contacts_router.get('/myinfo/contacts', response_class=HTMLResponse)
def contacts_list(req: Request, cpg: int = 1):
    if 'm' not in req.session:
        return RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)

    myinfo = MemberService.selectone_member(req.session['m'])
    uid = myinfo.userid
    qalist, cnt = QnaBoardService.select_questions(cpg, uid)

    # print('qalist > ', qalist)
    return templates.TemplateResponse('/myinfo/contacts/contacts.html', {
        'request': req,
        'qalist': qalist,
        'cpg': cpg,
        'stpg': 1,
        'allpage': 1,
        'baseurl': '/myinfo/contacts/',
        'my': myinfo
    })


#
# @myinfo_contacts_router.get('/myinfo/contacts', response_class=HTMLResponse)
# def contacts(req: Request):
#     if 'm' not in req.session:
#         return RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)
#
#     myinfo = MemberService.selectone_member(req.session['m'])
#     return templates.TemplateResponse('myinfo/contacts/contacts.html',{'request': req, 'my': myinfo})
#
# @myinfo_contacts_router.get('/myinfo/contacts/{cpg}', response_class=HTMLResponse)
# def list(req: Request, cpg: int):
#     # stpg = int((cpg - 1) / 10) * 10 + 1     # 페이지네이션 시작값
#     qalist, cnt = QnaBoardService.select_questions(cpg, uid)
#     # allpage = ceil( cnt / 25 )  # 총페이지수(올림해줌)
#     return templates.TemplateResponse('/myinfo/contacts/contacts.html',{'request': req, 'qalist': qalist,
#                                                                         'cpg': cpg, 'stpg': 1, 'allpage': 1, 'baseurl': '/myinfo/contacts/'})
#
#
#
# @myinfo_contacts_router.get('/myinfo/contacts', response_class=HTMLResponse)
# def contacts(req: Request):
#     if 'm' not in req.session:
#         return RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)
#
#     myinfo = MemberService.selectone_member(req.session['m'])
#     return list(req, cpg=1, uid=myinfo.userid)  # list() 함수 호출 시 'my' 인수 제외
#
# @myinfo_contacts_router.get('/myinfo/contacts/{cpg}', response_class=HTMLResponse)
# def list(req: Request, cpg: int, uid: str):
#     myinfo = MemberService.selectone_member(uid)  # uid로부터 myinfo 객체 얻기
#     qalist, cnt = QnaBoardService.select_questions(cpg, uid)
#     return templates.TemplateResponse('/myinfo/contacts/contacts.html', {'request': req, 'qalist': qalist,
#                                                                          'cpg': cpg, 'stpg': 1, 'allpage': 1,
#                                                                          'baseurl': '/myinfo/contacts/',
#                                                                          'my': myinfo})  # myinfo 객체를 템플릿에 추가








#
#
#
#
# @myinfo_contacts_router.get('/view/{gno}', response_class=HTMLResponse)
# def view(req: Request, gno:str):
#     gal = QnaBoardService.selectone_gallery(gno)
#     # GalleryService.update_count_gallery(gno)
#     return templates.TemplateResponse('/gallery/view.html',{'request': req, 'g': gal[0], 'ga': gal[1]})
#
#
# # 검색
# @myinfo_contacts_router.get('/list/{ftype}/{fkey}/{cpg}', response_class=HTMLResponse)
# def find(req: Request, ftype: str, fkey: str, cpg: int):
#     # stpg = int((cpg - 1) / 10) * 10 + 1     # 페이지네이션 시작값
#     # bdlist, cnt = BoardService.find_select_board(ftype, '%'+fkey+'%', cpg)
#     # allpage = ceil( cnt / 25 )  # 총페이지수(올림해줌)
#     return templates.TemplateResponse('/gallery/list.html',
#                                       {'request': req, 'gallist': None,'cpg': cpg,
#                                        'stpg': 1, 'allpage': 1, 'baseurl': f'/gallery/list/{ftype}/{fkey}/'})