from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from app.schemas.cart import NewCart
from app.services.cart import CartService

cart_router = APIRouter()

templates = Jinja2Templates(directory='views/templates')


@cart_router.get('/cart', response_class=HTMLResponse)
def cart(req: Request):
    clist = CartService.select_cart()
    return templates.TemplateResponse('shops/cart.html', {'request': req,
                                                          'clist': clist})


@cart_router.delete('/cart/{cno}')
def cart(cno: int):
    CartService.delete_cart(cno)
    return {"message": "success"}


@cart_router.post('/view')
def cartuser(cto: NewCart):
    result = CartService.insert_cart(cto)
    return result.rowcount
