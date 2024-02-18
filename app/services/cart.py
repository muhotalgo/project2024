from sqlalchemy import insert, select, delete

from app.dbfactory import Session
from app.models.cart import Cart
from app.models.product import Product


class CartService():
    @staticmethod
    def cart_convert(cto):
        data = cto.model_dump()
        c = Cart(**data)
        data = {'quantity': c.quantity, 'pno': c.pno}
        return data

    @staticmethod
    def insert_cart(cto):
        data = CartService.cart_convert(cto)
        with Session() as sess:
            stmt = insert(Cart).values(data)
            result = sess.execute(stmt)
            sess.commit()

        return result


    @staticmethod
    def select_cart():
        with Session() as sess:
            stmt = select(Cart.cno, Cart.quantity, Cart.pno, Product.exp, Product.name,
                          Product.height, Product.deps, Product.width, Product.price, Product.tumbimg, Product.ctno) \
                .join_from(Cart, Product)\
                .order_by(Cart.cno.desc()) \
                .offset(0).limit(20)
            result = sess.execute(stmt)
        return result


    @staticmethod
    def delete_cart(cno):
        with Session() as sess:
            stmt = delete(Cart).filter_by(cno=cno)
            result = sess.execute(stmt)
            sess.commit()
        return result