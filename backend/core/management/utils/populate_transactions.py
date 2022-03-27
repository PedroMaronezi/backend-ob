from core.models import User, MockedTransactions, Category
from core.models.transactions import (
    COMPLETED_AUTHORIZED_PAYMENT_TYPE,
    CREDIT_DEBIT_TYPE,
    TRANSACTION_TYPE,
    PARTIE_CNPJ_CPF_TYPE
)
from random import randrange

from dateutil.relativedelta import relativedelta
from django.utils import timezone

def insertTransactionsOnBankAccount(bankAccount):
    TRANSACTION_COUNT = 26
    now = timezone.now()

    categoryLen = Category.objects.count()
    allCategories = Category.objects.filter()

    for i in range(TRANSACTION_COUNT):

        randValue = randrange(10000)
        # Valor aleatório de 0 a 1000 unidades monetárias
        transactionValue = randValue/10

        # Data aleatória em intervalo de um ano (apenas passado)
        monthOffset = int(randValue*12/10000)
        dayOffset = int(randValue*28/10000)
        date = now - relativedelta(months=monthOffset, days=dayOffset)

        # Coloca uma categoria aleatória
        category = allCategories[i%categoryLen]

        MockedTransactions.objects.create(
            completedAuthorisedPaymentType=COMPLETED_AUTHORIZED_PAYMENT_TYPE.TRANSACAO_EFETIVADA,
            creditDebitType=CREDIT_DEBIT_TYPE.CREDITO if i%2==1 else CREDIT_DEBIT_TYPE.DEBITO,
            transactionName='Nome da transação',
            transactionType=TRANSACTION_TYPE.DOC,
            amount=transactionValue,
            transactionCurrency='BRL',
            transactionDate=date,
            partieCnpjCpf = "(adicionar campo de documento ao user)",
            partiePersonType =PARTIE_CNPJ_CPF_TYPE.PESSOA_FISICA,
            # partieCompeCode Não entendi bem o que é -> Confirmar e adicionar campo
            partieBranchCode=bankAccount.branchCode,
            partieNumber=bankAccount.number,
            partieCheckDigit=bankAccount.checkDigit,
            category=category
        )

def populate():
    print('Populando novas transações...')

    ricardo = User.objects.filter(email="ricardo@email.com").first()
    for account in ricardo.accounts.all():
        print(f"Criando transações para a conta do banco com usuário: {ricardo.name} | banco:{account.brandName}")
        insertTransactionsOnBankAccount(account)
