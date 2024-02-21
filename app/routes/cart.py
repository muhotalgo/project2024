from fastapi import APIRouter, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from app.schemas.cart import NewCart
from app.services.cart import CartService, OrderService
from app.services.member import MemberService

cart_router = APIRouter()

templates = Jinja2Templates(directory='views/templates')


@cart_router.get('/cart', response_class=HTMLResponse)
def cart(req: Request):
    muser = 0
    if 'm' in req.session:
        muser = MemberService.selectone_member(req.session['m']).userid

    userid = muser
    clist = CartService.select_cart(userid)
    row = CartService.select_cart(userid).fetchone()
    return templates.TemplateResponse('shops/cart.html', {'request': req, 'clist': clist, 'm': muser, 'row': row})


@cart_router.delete('/cart/{cno}')
def cart(cno: int):
    CartService.delete_cart(cno)
    return {"message": "success"}


# view에서 cart로 추가
@cart_router.post('/view')
def cartuser(cto: NewCart):
    result = CartService.insert_cart(cto)
    return result.rowcount


# cart에서 주문서로
@cart_router.get('/order', response_class=HTMLResponse)
def cartorder(req: Request):
    muser = 0
    if 'm' in req.session:
        muser = MemberService.selectone_member(req.session['m'])

    clist = CartService.select_cart(muser.userid)
    return templates.TemplateResponse('shops/order.html', {'request': req, 'clist': clist, 'm': muser})


@cart_router.post('/order')
def orderitem(mno: int = Form(), unitprice: int = Form(),
              pnos=Form(), quantitys=Form(), pdprices=Form()):
    print(mno, unitprice, pnos, quantitys, pdprices)
    result = OrderService.insert_order(mno, unitprice, pnos, quantitys, pdprices)
    return RedirectResponse('/shops/orderend', status_code=status.HTTP_302_FOUND)


# to orderend
@cart_router.get('/orderend', response_class=HTMLResponse)
def order(req: Request):
    muser = 0
    if 'm' in req.session:
        muser = MemberService.selectone_member(req.session['m'])
    odlist = OrderService.select_order(muser.mno)

    return templates.TemplateResponse('shops/orderend.html', {'request': req, 'm': muser, 'odlist': odlist})
