from app.models.order import Order
from app.models.member import Member
from app.models.product import Product
from app.dbfactory import Session
from sqlalchemy import select, insert, update, func, text
import requests
class OrdersService():
    @staticmethod
    def select_orders_and_products(cpg, mno):
        stnum = (cpg - 1) * 25
        with Session() as sess:
            # 주문 목록 및 상품 정보를 가져옴
            stmt = sess.query(Order.ono, Order.regdate, Order.status, Order.quantity, Order.pdprice, Order.pno, Product.name) \
                .join(Member, Order.mno == Member.mno) \
                .join(Product, Order.pno == Product.pno) \
                .filter(Member.mno == mno) \
                .order_by(Order.ono.desc()) \
                .offset(stnum).limit(25)
            result = sess.execute(stmt)

            # 주문 수를 가져옴
            cnt = sess.query(func.count(Order.ono)) \
                .join(Member, Order.mno == Member.mno) \
                .filter(Order.mno == Member.mno, Member.mno == mno) \
                .scalar()

        return result, cnt
