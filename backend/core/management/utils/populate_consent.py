from core.models import User, MockedTransactions, MockedConsent
from core.domain import consentController
from random import randrange

from dateutil.relativedelta import relativedelta
from django.utils import timezone


def populate():
    print('Populando novos consentimentos de usuários...')
    
    ricardo = User.objects.filter(email="ricardo@email.com").first()
    accounts = ricardo.accounts.all()
    consentController.createConsent(ricardo,accounts[0], ['ACCOUNTS_READ'], 2)
    consentController.createConsent(ricardo,accounts[1], ['ACCOUNTS_READ', 'ACCOUNTS_BALANCES_READ'], 2)
