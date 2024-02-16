from sqlalchemy import insert, select, update, func, or_

from app.dbfactory import Session
from app.models.product import Product


class ProductService():
    @staticmethod
    def product_convert(pdto):
        data = pdto.model_dump()
        pd = Product(**data)
        data = {'name': pd.name, 'exp': pd.exp, 'detail': pd.detail,
                'retail': pd.retail, 'pctoff': pd.pctoff, 'useyn': pd.useyn,
                'tumbimg': pd.tumbimg, 'catnum': pd.ctno}
        return data

    @staticmethod
    def select_list():
        with Session() as sess:
            stmt = select(Product.pno, Product.name, Product.exp, Product.detail, Product.price, Product.tumbimg,
                          Product.ctno) \
                .order_by(Product.pno.desc()) \
                .offset(0).limit(20)
            result = sess.execute(stmt)
        return result

    @staticmethod
    def selectone_prod(pno):
        with Session() as sess:
            stmt = select(Product).filter_by(pno=pno)
            result = sess.execute(stmt).first()
        return result
