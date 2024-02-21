from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from app.services.member import MemberService
from app.services.product import ProductService

product_router = APIRouter()
category_router = APIRouter()

templates = Jinja2Templates(directory='views/templates')


@product_router.get('/list', response_class=HTMLResponse)
def list(req: Request):
    pdlist = ProductService.select_list()
    return templates.TemplateResponse('shops/list.html', {'request': req,
                                                          'pdlist': pdlist})


# 카테고리별 상품 조회
@product_router.get('/list/{ctno}', response_class=HTMLResponse)
def list(req: Request, ctno: int):
    pdlist = ProductService.select_list_ctno(ctno)
    return templates.TemplateResponse('shops/list.html', {'request': req,
                                                          'pdlist': pdlist})


@product_router.get('/view/{pno}', response_class=HTMLResponse)
def view(req: Request, pno: str):
    muser = 0
    if 'm' in req.session:
        muser = MemberService.selectone_member(req.session['m'])
    pd = ProductService.selectone_prod(pno)[0]
    return templates.TemplateResponse('shops/view.html', {'request': req, 'pd': pd, 'm': muser})
