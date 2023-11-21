import sqlite3

from .depends.hash_user import check_password, hash_password
from .depends.validate import checkEmail
from .model_user import SigninUser, SignupUser
from .auth import create_jwt_token


class User:
    def __init__(self, db_name: str, db_table_name: str):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.db_table = db_table_name


    def db_isUser(self, title: str, user_info: str):
        self.cur.execute(
            f'''SELECT * FROM {self.db_table} WHERE {title}=?''', (user_info,))
        find_user = self.cur.fetchall()
        if not find_user:
            return False
        else:
            return find_user[0]

    def db_createUser(self, user: SignupUser):
        user_email = user.email
        user_username = user.username
        hashed_password = hash_password(user.password)

        self.cur.execute(f"INSERT INTO {self.db_table} (EMAIL, PASSWORD, USERNAME) VALUES(?, ?, ?)",
                         (user_email, hashed_password, user_username))
        self.con.commit()

    def signinUser(self, data: SigninUser):
        user_email = data.email
        user_password = data.password

        if not checkEmail(user_email):
            return {"result": False, "message": "이메일을 다시 확인해주세요."}

        response = self.db_isUser("EMAIL", user_email)
        
        if not (response):
            return {"result": False, "message": "존재하지 않는 이메일입니다."}

        else:
            db_user_password = response[2]
            db_user_username = response[3]

            if not check_password(user_password, db_user_password):
                return {"result": False, "message": "비밀번호를 다시 확인해주세요."}

            else:
                token_data = dict(email=user_email, username=db_user_username)
                access_token = create_jwt_token(token_data, 60)
                return {"result": True, "message": "로그인이 완료되었습니다.", "username": db_user_username, "access_token": access_token}

    def signupUser(self, user: SignupUser):
        user_email = user.email
        user_username = user.username

        if (self.db_isUser("EMAIL", user_email)):
            return {"result": False, "message": "이미 가입된 이메일입니다."}

        else:
            if self.db_isUser("USERNAME", user_username):
                return {"result": False, "message": "이미 존재하는 유저 이름입니다."}

            else:
                self.db_createUser(user)
                return {"result": True, "message": "회원가입이 완료되었습니다."}
