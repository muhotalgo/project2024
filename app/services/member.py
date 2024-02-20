from app.models.member import Member
from app.dbfactory import Session
from sqlalchemy import insert, update
import requests


class MemberService():
    @staticmethod
    def member_convert(mdto):
        # 클라이언트에서 전달받은 데이터를 dict형으로 변환
        data = mdto.model_dump()
        mb = Member(**data)
        data = {'userid': mb.userid, 'passwd': mb.passwd, 'zipcode': mb.zipcode, 'address1': mb.address1, 'address2': mb.address2,
                'name': mb.name, 'phone': mb.phone, 'email': mb.email}

        return data

    @staticmethod
    def insert_member(mdto):
        # 변환된 회원정보를 member 테이블에 저장
        data = MemberService.member_convert(mdto)
        with Session() as sess:
            stmt = insert(Member).values(data)
            result = sess.execute(stmt)
            sess.commit()

        return result


    @staticmethod
    def check_login(userid, passwd):
        with Session() as sess:
            # Member테이블에서 아이디로 회원 조회후
            result = sess.query(Member).filter_by(userid=userid).scalar()
            # 회원이 존재한다면
            # 실제 회원이 존재하고 비밀번호가 일치한다면
            if result and passwd == result.passwd:
                return result
        return None

    @staticmethod
    def selectone_member(userid):
        with Session() as sess:
            result = sess.query(Member).filter_by(userid=userid).scalar()
            return result


    # 아이디,전화번호,이메일 중복 체크
    @staticmethod
    def check_duplicate(field_name: str, value: str):
        with Session() as sess:
            if field_name == 'userid':
                result = sess.query(Member).filter_by(userid=value).first()
            elif field_name == 'phone':
                result = sess.query(Member).filter_by(phone=value).first()
            elif field_name == 'email':
                result = sess.query(Member).filter_by(email=value).first()
            else:
                # 지원되지 않는 필드명에 대한 처리
                return None
            return result


    # 회원정보수정
    @staticmethod
    def member_modify_convert(mdto):
        # 클라이언트에서 전달받은 데이터를 dict형으로 변환
        data = mdto.model_dump()
        data.pop('response') # captcha 확인용변수 response는 제거 # 캡챠 사용시 주석처리 제거
        mb = Member(**data)
        # data = {'userid': mb.userid, 'passwd': mb.passwd, 'zipcode': mb.zipcode, 'address1': mb.address1, 'address2': mb.address2,
        #         'name': Member.name, 'phone': Member.phone, 'email': mb.email}
        data = {'userid': mb.userid, 'passwd': mb.passwd, 'zipcode': mb.zipcode, 'address1': mb.address1, 'address2': mb.address2, 'email': mb.email}

        return data

    @staticmethod
    def modify_member(mdto):
        # 변환된 회원정보를 member 테이블에 저장
        data = MemberService.member_modify_convert(mdto)
        # print('modify data > ', data)

        with Session() as sess:
            stmt = update(Member).where(Member.userid == data['userid']).values(data)
            result = sess.execute(stmt)
            sess.commit()

        return result

#
#         result = sess.query(Member).filter_by(userid=value).first()
#
# member = session.query(Member).filter(Member.userid == 'abc').first()
#
#         with Session() as sess:
#             result = sess.query(Member).filter_by(userid=data.userid).first()
#
#
# stmt = insert(Member).values(data)
#             result = sess.execute(stmt)
#             sess.commit()
#
#         with Session() as sess:
#             stmt = insert(Member).values(data)
#             result = sess.execute(stmt)
#             sess.commit()
#
#         return result



    # hcaptcha recaptcha 확인 url
    # https://api.hcaptcha.com/siteverify?secret=비밀키&response=응답토큰
    @staticmethod
    def check_captcha(mdto):
        data = mdto.model_dump()    # 클라이언트가 보낸 객체를 dict로 변경
        req_url = 'https://api.hcaptcha.com/siteverify'
        # hcaptcha 시크릿 키 입력
        params = { 'secret': 'ES_af6fcc3ee1f94c2293543b940be42321',
                   'response': data['response'] }
        res = requests.get(req_url, params=params)
        result = res.json()

        return result['success']
        # return True