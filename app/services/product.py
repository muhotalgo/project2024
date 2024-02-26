from sqlalchemy import insert, select, update, func, or_

from app.dbfactory import Session
from app.models.product import Product
from app.models.category import Category


class ProductService():
    @staticmethod
    def product_convert(pdto):
        data = pdto.model_dump()
        pd = Product(**data)
        data = {'name': pd.name, 'exp': pd.exp, 'detail': pd.detail,
                'retail': pd.retail, 'pctoff': pd.pctoff, 'useyn': pd.useyn,
                'tumbimg': pd.tumbimg, 'ctno': pd.ctno}
        return data

    @staticmethod
    def category_convert(ctto):
        ctdata = ctto.model_dump()
        ct = Product(**ctdata)
        ctdata = {'kctname': ct.kctname, 'sctname': ct.sctname, 'catcod': ct.catcod}
        return ctdata

    # 전체 상품 조회
    @staticmethod
    def select_list():
        with Session() as sess:
            stmt = select(Product.pno, Product.name, Product.exp, Product.detail, Product.price, Product.tumbimg,
                          Product.ctno)\
                .order_by(Product.pno) \
                .offset(0).limit(20)
            result = sess.execute(stmt)
        return result

    # 카테고리별 상품 조회
    @staticmethod
    def select_list_ctno(ctno):
        with Session() as sess:
            stmt = select(Product.pno, Product.name, Product.exp, Product.detail, Product.price, Product.tumbimg,
                          Product.ctno, Category.kctname, Category.sctname, Category.catcod).join_from(Product,
                                                                                                       Category) \
                .order_by(Product.pno).where(Product.ctno == ctno) \
                .offset(0).limit(20)
            result = sess.execute(stmt)
            cate = sess.execute(stmt).first()

        return result, cate

    # 상품명 검색 조회 - 상품번호, 상품이름, 상품 간략정보, 상품 상세정보에서 조회
    @staticmethod
    def find_select_list(skey):
        with Session() as sess:
            stmt = select(Product.pno, Product.name, Product.exp, Product.detail, Product.price, Product.tumbimg,
                          Product.ctno)

            myfilter = or_(Product.pno.like(skey), Product.name.like(skey), Product.exp.like(skey),
                           Product.detail.like(skey))

            stmt = stmt.filter(myfilter) \
                .order_by(Product.pno).offset(0).limit(20)
            result = sess.execute(stmt)

        return result

    # 상품 상세페이지 이동
    @staticmethod
    def selectone_prod(pno):
        with Session() as sess:
            stmt = select(Product).filter_by(pno=pno)
            result = sess.execute(stmt).first()
        return result
