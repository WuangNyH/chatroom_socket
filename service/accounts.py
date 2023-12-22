from model.accounts import Account
from serializer.accounts import AccountSchema, AccountLogin
from core.Database import SessionLocal
import hashlib


class AccountService:
    def __init__(self):
        self.db = SessionLocal()

    def convert_md5_hash(self, password):
        return hashlib.md5(password.encode()).hexdigest()

    def create_account(self, data: AccountSchema):
        new_account = Account(**data.model_dump())
        new_account.password = self.convert_md5_hash(new_account.password)
        self.db.add(new_account)
        self.db.commit()
        self.db.close()
        return new_account

    def login(self, data: AccountLogin):
        data_user = data.model_dump()
        data_user['password'] = self.convert_md5_hash(data_user['password'])
        user = self.db.query(Account).filter_by(email=data_user.get("email")).first()

        if not user:
            raise ValueError("Account does not exist")

        if not user.password == data_user["password"]:
            raise ValueError("Incorrect password")

        return user.nickname
