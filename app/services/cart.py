from sqlalchemy import insert, select, delete, update
from datetime import datetime

from app.dbfactory import Session
from app.models.cart import Cart
from app.models.order import Order
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
            existing_cart = None
            if CartService.select_cart(data['userid']):
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
    def order_convert(oto):
        data = oto.model_dump()
        o = Order(**data)
        data = {'mno': o.mno, 'status': o.status,
                'unitprice': o.unitprice, 'pno': o.pno,
                'quantity': o.quantity, 'pdprice': o.pdprice, 'gono': o.gono}
        return data

    # 장바구니 -> order
    @staticmethod
    def insert_order(mno, unitprice, pnos, quantitys, pdprices):
        pnos = pnos.split(",")
        quantitys = quantitys.split(",")
        pdprices = pdprices.split(",")
        gono = datetime.today().strftime('%Y%m%d%H%M%S')

        with Session() as sess:
            for idx, i in enumerate(pnos):
                # 주문 등록
                data = {'mno': mno, 'unitprice': unitprice,
                        'pno': pnos[idx], 'quantity': quantitys[idx], 'pdprice': pdprices[idx], 'gono': gono}
                stmt = insert(Order).values(data)
                result = sess.execute(stmt)
                sess.commit()

                # 장바구니 지우기
                stmt = delete(Cart).filter_by(cno=Cart.cno)
                result = sess.execute(stmt)
                sess.commit()

        return result

    # 장바구니 -> orderdr
    @staticmethod
    def insert_orderdr(mno, unitprice, pnos, quantitys, pdprices):
        pnos = pnos.split(",")
        quantitys = quantitys.split(",")
        pdprices = pdprices.split(",")
        gono = datetime.today().strftime('%Y%m%d%H%M%S')

        with Session() as sess:
            for idx, i in enumerate(pnos):
                # 주문 등록
                data = {'mno': mno, 'unitprice': unitprice,
                        'pno': pnos[idx], 'quantity': quantitys[idx], 'pdprice': pdprices[idx], 'gono': gono}
                stmt = insert(Order).values(data)
                result = sess.execute(stmt)
                sess.commit()

        return result

    # 주문정보 조회
    @staticmethod
    def select_order(mno):
        with Session() as sess:
            stmt = select(Order.ono, Order.mno, Order.status, Order.unitprice, Order.quantity,
                          Order.pdprice, Order.regdate, Order.pno, Product.exp, Product.name,
                          Product.height, Product.deps, Product.width, Product.price, Product.tumbimg, Product.ctno) \
                .join_from(Order, Product).where(mno == Order.mno) \
                .order_by(Order.ono) \
                .offset(0).limit(20)
            result = sess.execute(stmt)
        return result

    # 주문정보 하나 조회
    @staticmethod
    def select_orderone(mno):
        with Session() as sess:
            stmt = select(Order).filter_by(mno=mno).order_by(Order.ono.desc())
            result = sess.execute(stmt).first()
        return result
