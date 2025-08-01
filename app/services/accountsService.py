import uuid
from typing import Dict
from django.utils.timezone import datetime, now
from app.repositories.accountsRepo import AccountsRepo
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password, make_password
from app.utils.redisClient import RedisClient
import logging

log = logging.getLogger(__name__)


class AccountsService:
    @staticmethod
    def is_valid_email(email: str):
        if not email or "@" not in email or "." not in email:
            return False
        return email.count("@") == 1

    @staticmethod
    def find_all():
        try:
            return AccountsRepo.get_all()
        except Exception as e:
            log.error(f"ERROR: from find all account: {e}")
            return None

    @staticmethod
    def find_by_id(account_id: str):
        try:
            if account_id and str(account_id).strip():
                uuid_obj = uuid.UUID(account_id)
                return AccountsRepo.get_by_id(uuid_obj)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_id account: {e}")
            return None

    @staticmethod
    def find_by_username(username: str):
        try:
            if username and str(username).strip():
                return AccountsRepo.get_by_username(username)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_username account: {e}")
            return None

    @staticmethod
    def find_by_nickname(nickname: str):
        try:
            if nickname and str(nickname).strip():
                return AccountsRepo.filter_by_nickname(nickname)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_nickname account: {e}")
            return None

    @staticmethod
    def find_by_email(email: str):
        try:
            if AccountsService.is_valid_email(email):
                return AccountsRepo.get_by_email(email)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_email account: {e}")
            return None

    @staticmethod
    def find_by_status(is_active: bool = True):
        try:
            return AccountsRepo.filter_by_status(is_active)
        except Exception as e:
            log.error(f"ERROR: from find_by_status account: {e}")
            return None

    @staticmethod
    def find_by_date_created(date: datetime = None):
        try:
            return AccountsRepo.filter_by_date_created(date or now())
        except Exception as e:
            log.error(f"ERROR: from find_by_created_date account: {e}")
            return None

    @staticmethod
    def find_by_birth_day(date: datetime):
        try:
            if date:
                return AccountsRepo.filter_by_birth_day(date)
            return None
        except Exception as e:
            log.error(f"ERROR: from find_by_birth_day account: {e}")
            return None

    @staticmethod
    def create(data: Dict):
        try:
            username = data.get("username")
            email = data.get("email")

            if AccountsRepo.get_by_username(username):
                log.error(f"ERROR: username '{username}' already exists.")
                return None

            if AccountsRepo.get_by_email(email):
                log.error(f"ERROR: email '{email}' already exists.")
                return None

            return AccountsRepo.do_create(data)
        except Exception as e:
            log.error(f"ERROR: from create account: {e}")
            return None

    @staticmethod
    def update(account_id: str, data: Dict):
        try:
            if account_id and str(account_id).strip() and any(data.values()):
                account = AccountsService.find_by_id(account_id)
                if not account:
                    return None
                return AccountsRepo.do_update(account, data)
            return None
        except Exception as e:
            log.error(f"ERROR: from update account: {e}")
            return None

    @staticmethod
    def delete(account_id: str):
        try:
            if account_id and str(account_id).strip():
                account = AccountsService.find_by_id(account_id)
                if not account:
                    return None
                return AccountsRepo.do_delete(account)
            return None
        except Exception as e:
            log.error(f"ERROR: from delete account: {e}")
            return None

    @staticmethod
    def hard_delete(account_id: str):
        try:
            if account_id and str(account_id).strip():
                account = AccountsService.find_by_id(account_id)
                if not account:
                    return False
                return AccountsRepo.do_hard_delete(account)
            return False
        except Exception as e:
            log.error(f"ERROR: from hard_delete account: {e}")
            return False

    @staticmethod
    def login(data: Dict):
        try:
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            account = None
            if username:
                account = AccountsService.find_by_username(username)
            elif email:
                account = AccountsService.find_by_email(email)

            if account and check_password(str(password), account.password):
                refresh = RefreshToken.for_user(account)
                rd = RedisClient.instance()
                rd.add(
                    key=f"rft_{account.id}",
                    value=str(refresh),
                    expire_sec=7 * 24 * 60 * 60,
                )
                return {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                }
            return None
        except Exception as e:
            log.error(f"ERROR: from login: {e}")
            return None

    @staticmethod
    def registry(data: dict):
        try:
            username = str(data.get("username"))
            email = str(data.get("email"))

            if not AccountsService.find_by_username(
                username
            ) and not AccountsService.find_by_email(email):
                data["password"] = make_password(str(data.get("password")))
                return AccountsService.create(data)

            return None

        except Exception as e:
            log.error(f"ERROR: when registry: {str(e)}")
            return None

    @staticmethod
    def restock_token(refresh_token: str):
        try:
            token = RefreshToken(refresh_token)
            account_id = token["user_id"]
            rd = RedisClient.instance()
            if rd.exists(f"rft_{account_id}") != 0:
                account = AccountsService.find_by_id(account_id)
                if not account:
                    return None
                refresh = RefreshToken.for_user(account)
                access = refresh.access_token
                rd.add(
                    key=f"rft_{account.id}",
                    value=str(refresh),
                    expire_sec=7 * 24 * 60 * 60,
                )
                return {"access_token": str(access), "refresh_token": str(refresh)}
            return None
        except Exception as e:
            log.error(f"ERROR: Lỗi khi cấp lại token: {str(e)}")
            return None
