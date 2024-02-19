from sqlalchemy import insert, select, delete, update

from app.dbfactory import Session
from app.models.cart import Cart
from app.models.order import Order, OrderItem
from app.models.product import Product


class CartService():
    @staticmethod
    def cart_convert(cto):
        data = cto.model_dump()
        c = Cart(**data)
        data = {'quantity': c.quantity, 'userid': c.userid, 'pno': c.pno}
        return data

    # 장바구니 추가
    @staticmethod
    def insert_cart(cto):
        data = CartService.cart_convert(cto)
        with Session() as sess:

            # 장바구니 중복확인
            existing_cart = sess.query(Cart).filter_by(pno=data['pno']).first()

            if existing_cart:
                new_quantity = existing_cart.quantity + 1  # 기존 수량에 1을 추가
                stmt = update(Cart).where(Cart.pno == data['pno']).values(quantity=new_quantity)
                result = sess.execute(stmt)
            else:
                stmt = insert(Cart).values(data)
                result = sess.execute(stmt)

            sess.commit()

        return result

    @staticmethod
    def select_cart(userid):
        with Session() as sess:
            stmt = select(Cart.cno, Cart.quantity, Cart.pno, Cart.userid, Product.exp, Product.name,
                          Product.height, Product.deps, Product.width, Product.price, Product.tumbimg, Product.ctno) \
                .join_from(Cart, Product).where(Cart.userid == userid) \
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


class OrderService():
    @staticmethod
    def orderitem_convert(oito):
        data = oito.model_dump()
        oi = OrderItem(**data)
        data = {'pno': oi.pno, 'quantity': oi.quantity, 'pdprice': oi.pdprice, 'unitno': oi.unitno}
        return data

    # 장바구니 -> orderitem -> order
    @staticmethod
    def insert_orderitem(oito):
        data = OrderService.orderitem_convert(oito)
        with Session() as sess:
            stmt = insert(OrderItem).values(data)
            result = sess.execute(stmt)

            sess.commit()

        return result
