from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status

from app.services.member import MemberService
from app.services.orders import OrdersService

myinfo_orders_router = APIRouter()

# jinja2 설정
templates = Jinja2Templates(directory='views/templates')
# myinfo_orders_router.mount('/static', StaticFiles(directory='views/static'), name='static')


# 마이페이지 / 내 주문 내역 보기 (list)
# 마이페이지 / 내 주문 내역
@myinfo_orders_router.get('/myinfo/orders/{cpg}', response_class=HTMLResponse)
@myinfo_orders_router.get('/myinfo/orders', response_class=HTMLResponse)
def orderslist(req: Request, cpg: int = 1):
    if 'm' not in req.session:
        return RedirectResponse(url='/login', status_code=status.HTTP_303_SEE_OTHER)

    myinfo = MemberService.selectone_member(req.session['m'])
    mno = myinfo.mno
    odlist, cnt = OrdersService.select_orders_and_products(cpg, mno)




    return templates.TemplateResponse('/myinfo/orders.html', {
        'request': req,
        'odlist': odlist,
        # 'pnames': 'TEST_HERE',
        'cpg': cpg,
        'stpg': 1,
        'allpage': 1,
        'baseurl': '/myinfo/orders/',
        'my': myinfo
    })