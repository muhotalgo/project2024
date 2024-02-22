from app.models.contact import Qna
from app.models.member import Member
from app.dbfactory import Session
from sqlalchemy import select, insert, func
import requests




class QnaBoardService():
    @staticmethod
    def qnaboard_convert(bdto):
        # 클라이언트에서 전달받은 데이터를 dict형으로 변환
        data = bdto.model_dump()
        data.pop('response') # captcha 확인용변수 response는 제거
        bd = Qna(**data)   # 보드 클래스와 스키마에 정해져있는거랑 다름. response가 있었는데 여기는 response를 뺴줘야함
        data = {'title': bd.title, 'userid': bd.userid, 'contents': bd.contents}

        return data


    @staticmethod
    def insert_board(bdto):
        # 변환된 게시글 정보를 qna 테이블에 저장
        data = QnaBoardService.qnaboard_convert(bdto)

        with Session() as sess:
            stmt = insert(Qna).values(data)
            result = sess.execute(stmt)
            sess.commit()

        return result


    #
    # @staticmethod
    # def check_login(userid, passwd):
    #     with Session() as sess:
    #         # Member테이블에서 아이디로 회원 조회후
    #         result = sess.query(Member).filter_by(userid=userid).scalar()
    #         # 회원이 존재한다면
    #         # 실제 회원이 존재하고 비밀번호가 일치한다면
    #         if result and passwd == result.passwd:
    #             return result
    #     return None
    #
    # @staticmethod
    # def selectone_member(userid):
    #     with Session() as sess:
    #         result = sess.query(Member).filter_by(userid=userid).scalar()
    #         return result
    #
    #
    # # 아이디,전화번호,이메일 중복 체크
    # @staticmethod
    # def check_duplicate(field_name: str, value: str):
    #     with Session() as sess:
    #         if field_name == 'userid':
    #             result = sess.query(Member).filter_by(userid=value).first()
    #         elif field_name == 'phone':
    #             result = sess.query(Member).filter_by(phone=value).first()
    #         elif field_name == 'email':
    #             result = sess.query(Member).filter_by(email=value).first()
    #         else:
    #             # 지원되지 않는 필드명에 대한 처리
    #             return None
    #         return result



    # hcaptcha recaptcha 확인 url
    # https://api.hcaptcha.com/siteverify?secret=비밀키&response=응답토큰
    @staticmethod
    def check_captcha(resp):
        data = resp.model_dump()    # 클라이언트가 보낸 객체를 dict로 변경
        req_url = 'https://api.hcaptcha.com/siteverify'
        # hcaptcha 시크릿 키 입력
        params = { 'secret': 'ES_af6fcc3ee1f94c2293543b940be42321',
                   'response': data['response'] }
        res = requests.get(req_url, params=params)
        result = res.json()

        return result['success']
        # return True


    @staticmethod
    def select_questions(cpg, uid):
        stnum = (cpg - 1) * 25
        user_id = uid
        with Session() as sess:
            cnt = sess.query(func.count(Qna.qno)) \
                .join(Member, Qna.userid == Member.userid) \
                .filter(Qna.userid == Member.userid, Member.userid == user_id) \
                .scalar()

            stmt = sess.query(Qna.qno, Qna.userid, Qna.title, Qna.regdate) \
                .join(Member, Qna.userid == Member.userid) \
                .filter(Member.userid == user_id) \
                .order_by(Qna.qno.desc()) \
                .offset(stnum).limit(25)
            result = sess.execute(stmt)

        return result, cnt


    @staticmethod
    def selectone_board(qno):
        with Session() as sess:

            stmt = select(Qna).filter_by(qno=qno)
            result = sess.execute(stmt).first()

            return result
