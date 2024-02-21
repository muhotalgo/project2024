from app.models.contact import Contact
from app.dbfactory import Session
from sqlalchemy import insert, select, update, func, or_
import requests

class ContactService():
    @staticmethod
    def contact_convert(cdto):
        data = cdto.model_dump()
        data.pop('response')        # captcha 확인용 변수 response는 제거
        cd = Contact(**data)
        data = {'userid':cd.userid, 'title':cd.title, 'contents':cd.contents}
        return data


    @staticmethod
    def insert_board(cdto):
        data = ContactService.contact_convert(cdto)
        with Session() as sess:
            stmt = insert(Contact).values(data)
            result = sess.execute(stmt)
            sess.commit()

            return result

    @staticmethod
    def select_contact(cpg):
        stnum = (cpg - 1) * 25
        with Session() as sess:

            cnt = sess. query(func.count(Contact.cno)).scalar()   # 총 게시글 수

            stmt = select(Contact.cno, Contact.title, Contact.userid, Contact.regdate, Contact.views) \
                .order_by(Contact.cno.desc()) \
                .offset(stnum).limit(25)
            result = sess.execute(stmt)

            return result, cnt


    @staticmethod
    def find_select_contact(ftype, fkey, cpg):
        stnum = (cpg - 1) * 25
        with Session() as sess:
            stmt = select(Contact.bno, Contact.title, Contact.userid, Contact.regdate, Contact.views)

            # 동적 쿼리 작성 - 조건에 다라 where절이 바뀜
            myfilter = Contact.title.like(fkey)
            if ftype == 'userid': myfilter = Contact.userid.like(fkey)
            elif ftype == 'contents': myfilter = or_(Contact.title.like(fkey), Contact.contents.like(fkey))

            stmt = stmt.filter(myfilter) \
                .order_by(Contact.bno.desc()).offset(stnum).limit(25)
            result = sess.execute(stmt)

            cnt = sess. query(func.count(Contact.bno)).filter(myfilter).scalar()   # 총 게시글 수

            return result, cnt



    @staticmethod
    def selectone_contact(cno):
        with Session() as sess:

            stmt = select(Contact).filter_by(cno=cno)
            result = sess.execute(stmt).first()

            return result


    @staticmethod
    def update_count_contact(cno):
        with Session() as sess:
            stmt = update(Contact).filter_by(cno=cno).values(views=Contact.views+1)
            result = sess.execute(stmt)
            sess.commit()

            return result

    # google recaptcha 확인 url
    # https://www.google.com/recaptcha/api/siteverify?secret=비밀키&response=응답토큰
    @staticmethod
    def check_captcha(cdto):
        data = cdto.model_dump()    # 클라이언트가 보낸 객체를 dict로 변환
        req_url = 'https://www.google.com/recaptcha/api/siteverify'
        params = { 'secret': '', # 시크릿 키
                   'response': data['response'] }

        res = requests.get(req_url, params=params)
        result = res.json()
        # print('check', result)

        # return result['success']
        return True
