from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from app.services.product import ProductService

product_router = APIRouter()

templates = Jinja2Templates(directory='views/templates')


# @product_router.get('/list', response_class=HTMLResponse)
# def product(req: Request):
#     return templates.TemplateResponse('shops/product/list.html', {'request': req})

@product_router.get('/list', response_class=HTMLResponse)
def list(req: Request):
    pdlist = ProductService.select_list()
    return templates.TemplateResponse('shops/product/list.html', {'request': req,
                                              'pdlist': pdlist})


@product_router.get('/view/{prodno}', response_class=HTMLResponse)
def view(req: Request, prodno: str):
    pd = ProductService.selectone_prod(prodno)[0]
    return templates.TemplateResponse('shops/product/view.html', {'request': req, 'pd': pd})