
from fastapi import APIRouter, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status


from app.schemas.member import NewMember, ModiMember
from app.services.member import MemberService

member_router = APIRouter()

# jinja2 설정
templates = Jinja2Templates(directory='views/templates')
member_router.mount('/static', StaticFiles(directory='views/static'), name='static')


@member_router.get('/join', response_class=HTMLResponse)
def join(req: Request):
    return templates.TemplateResponse('join.html', {'request': req})

# DB로 제출하기 / 회원가입 완료시키기
@member_router.post('/join')
def joincheck(mdto: NewMember):
    result = MemberService.insert_member(mdto)
    return result.rowcount

@member_router.get('/joinok', response_class=HTMLResponse)
def joinok(req: Request):
    return templates.TemplateResponse('joinok.html', {'request': req})

@member_router.get('/login', response_class=HTMLResponse)
def login(req: Request):
    return templates.TemplateResponse('login.html', {'request': req})

# 회원가입시 아이디, 전화번호, 이메일 중복확인
@member_router.get('/check/{check_type}/{value}')
def signupcheck(req: Request, check_type: str, value: str):
    result = None

    if check_type == 'uid':
        result = MemberService.check_duplicate('userid', value)
    elif check_type == 'phone':
        result = MemberService.check_duplicate('phone', value)
    elif check_type == 'email':
        result = MemberService.check_duplicate('email', value)
    else:
        # 잘못된 유형의 중복 확인 요청에 대한 처리
        return 'invalid'

    if result:
        return 'yes'
    else:
        return 'no'


@member_router.post('/login', response_class=HTMLResponse)
def login(req: Request, userid: str = Form(), passwd: str = Form()):
    result = MemberService.check_login(userid, passwd)
    if result:
        # 세션처리 - 회원아이디를 세션에 등록
        req.session['m'] = result.userid
        return RedirectResponse(url='/myinfo', status_code=status.HTTP_303_SEE_OTHER)
    else:
        return HTMLResponse("""
            <script>
                alert('로그인에 실패했습니다. 아이디 혹은 비밀번호를 확인하세요.');
                window.location.href = '/login';
            </script>
        """)

@member_router.get('/logout')
def logout(req: Request):
    req.session.clear()     # 생성된 세션객체 제거
    return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)

# 마이페이지
@member_router.get('/myinfo', response_class=HTMLResponse)
def myinfo(req: Request):
    if 'm' not in req.session:
        return RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)

    myinfo = MemberService.selectone_member(req.session['m'])
    return templates.TemplateResponse('myinfo.html',{'request': req, 'my': myinfo})


# 마이페이지 항목 수정 페이지
@member_router.get('/myinfo/modify', response_class=HTMLResponse)
def checkmodify(req: Request):
    if 'm' not in req.session:
        return RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)

    myinfo = MemberService.selectone_member(req.session['m'])
    return templates.TemplateResponse('myinfo/modify.html',{'request': req, 'my': myinfo})


# DB로 수정하기 / 수정 완료시키기
@member_router.post('/myinfo/modify')
def modify(mdto: ModiMember):
    res_url = '/captcha_error'
    if MemberService.check_captcha(mdto):    # captcha 체크가 true 라면 아래진행
        result = MemberService.modify_member(mdto)
        res_url = '/write_error'
        if result.rowcount > 0: res_url = '/myinfo'
    return RedirectResponse(res_url, status_code=status.HTTP_302_FOUND)

    #     return HTMLResponse("""
    #             <script>
    #                 alert('회원정보수정에 성공했습니다.');
    #                 window.location.href = '/myinfo';
    #             </script>
    #         """)
    # else:
    #     raise HTTPException(status_code=500, detail='회원정보 수정에 실패했습니다.')


# 마이페이지 / 주문내역

@member_router.get('/myinfo/orders', response_class=HTMLResponse)
def orders(req: Request):
    if 'm' not in req.session:
        return RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)

    myinfo = MemberService.selectone_member(req.session['m'])
    # orders = MemberService.
    return templates.TemplateResponse('myinfo/orders.html',{'request': req, 'my': myinfo, 'od': orders})



# 마이페이지 / 내 질문 내역
@member_router.get('/myinfo/contacts', response_class=HTMLResponse)
def contacts(req: Request):
    if 'm' not in req.session:
        return RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)

    myinfo = MemberService.selectone_member(req.session['m'])
    return templates.TemplateResponse('myinfo/contacts.html',{'request': req, 'my': myinfo})

