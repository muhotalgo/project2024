import requests
from sqlalchemy import insert, select, update, func, or_
from app.dbfactory import Session
from app.models.contact import Notice
from app.models.contact import Qna


class QnaService:
    @staticmethod
    def select_Notice(cpg):
        stnum = (cpg - 1) * 25
        with Session() as sess:
            stmt = select(Notice.nno, Notice.regdate, Notice.title) \
                .order_by(Notice.nno.desc()).offset(stnum).limit(25)
            result = sess.execute(stmt)

        return result

