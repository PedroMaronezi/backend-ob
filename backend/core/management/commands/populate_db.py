from django.core.management.base import BaseCommand, CommandError
from core.management.utils import ( populate_users, populate_accounts, populate_category, populate_transactions, populate_consent , populate_permissions)

class Command(BaseCommand):
    help = 'Popula o banco de dados com itens necessários ou úteis para execução de testes em ambiente de desenvolvimento'

    def handle(self, *args, **options):
        populate_users.populate()
        populate_accounts.populate()
        populate_category.populate()
        populate_transactions.populate()
        populate_permissions.populate()
        populate_consent.populate()