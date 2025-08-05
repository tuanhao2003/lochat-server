import uuid
from django.utils.timezone import datetime, now
from app.entities.accounts import Accounts
from django.core.paginator import Paginator
import logging

log = logging.getLogger(__name__)


class AccountsRepo:
    @staticmethod
    def get_all():
        try:
            return Accounts.objects.all()
        except Exception as e:
            log.error("ERROR: from get all account: " + str(e))
            return None


    @staticmethod
    def get_by_id(account_id: uuid.UUID):
        try:
            return Accounts.objects.get(id=account_id)
        except Exception as e:
            log.error("ERROR: from get account by id: " + str(e))
            return None

    @staticmethod
    def get_by_username(username: str):
        try:
            return Accounts.objects.get(username=username)
        except Exception as e:
            log.error("ERROR: from get by username: " + str(e))
            return None
        
    @staticmethod
    def filter_by_nickname(nickname: str):
        try:
            return Accounts.objects.get(nickname__icontains=nickname)
        except Exception as e:
            log.error("ERROR: from get by nickname: " + str(e))
            return None
            
    @staticmethod
    def get_by_email(email: str):
        try:
            return Accounts.objects.get(email=email)
        except Exception as e:
            log.error("ERROR: from get by email: " + str(e))
            return None

    @staticmethod
    def filter_by_date_created(date: datetime):
        try:
            return Accounts.objects.filter(created_at=date)
        except Exception as e:
            log.error("ERROR: from filter by email: " + str(e))
            return None

    @staticmethod
    def filter_by_status(status: bool = True):
        try:
            return Accounts.objects.filter(is_active=status)
        except Exception as e:
            log.error("ERROR: from filter by status: " + str(e))
            return None

    @staticmethod
    def filter_by_birth_day(date: datetime):
        try:
            return Accounts.objects.filter(birth = date)
        except Exception as e:
            log.error("ERROR: from filter by birth day: " + str(e))
            return None

    @staticmethod
    def do_create(data: dict):
        try:
            return Accounts.objects.create(**data)
        except Exception as e:
            log.error("ERROR: from do create account: " + str(e))
            return None

    @staticmethod
    def do_update(account: Accounts, data: dict):
        try:
            for field, value in data.items():
                setattr(account, field, value)
            account.updated_at = now
            account.save(update_fields=data.keys()) 
            return account
        except Exception as e:
            log.error("ERROR: from update account: " + str(e))
            return None

    @staticmethod
    def do_delete(account: Accounts):
        try:
            account.is_active = False
            account.updated_at = now
            account.save()
            return account
        except Exception as e:
            log.error("ERROR: from soft delele account: " + str(e))
            return None

    @staticmethod
    def do_hard_delete(account: Accounts):
        try:
            account.delete()
            return True
        except Exception as e:
            log.error("ERROR: from hard delete account: " + str(e))
            return False

    @staticmethod
    def get_all_paginated(page=1, page_size=10):
        try:
            queryset = Accounts.objects.all().order_by('-created_at')

            paginator = Paginator(queryset, page_size)

            items = paginator.page(page)

            return {
                "pages_count": paginator.num_pages,
                "current_page": items.number,
                "page_content": list(items)
            }
        except Exception as e:
            log.error("ERROR: from get_all paginated accounts: " + str(e))
            return None