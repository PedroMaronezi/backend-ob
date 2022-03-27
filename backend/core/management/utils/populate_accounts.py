from core.models import User, MockedBankAccount
from core.models.bankAccounts import ACCOUNT_TYPES

BANK_DATA = [
    {
        "branchName": "itau", #TODO: Confirmar se esse campo realmente é o nome do banco ou se é o nosso nome!
        "companyCnpj": "1111111111", # CNPJ do banco
        "branchCode": "111" # código da agência
    },
    {
        "branchName": "santander",
        "companyCnpj": "2222222222",
        "branchCode": "222"
    },
    {
        "branchName": "Nubank",
        "companyCnpj": "4444444444444",
        "branchCode": "444"
    },
    {
        "branchName": "Bradesco",
        "companyCnpj": "5555555555",
        "branchCode": "555"
    },
    {
        "branchName": "Banco do Brasil",
        "companyCnpj": "6666666666",
        "branchCode": "666"
    },
    {
        "branchName": "Mercado Pago",
        "companyCnpj": "7777777777",
        "branchCode": "777"
    },
    {
        "branchName": "Banco Inter",
        "companyCnpj": "8888888888",
        "branchCode": "888"
    },
    {
        "branchName": "N26",
        "companyCnpj": "9999999999",
        "branchCode": "999"
    },
    {
        "branchName": "Wiscredi",
        "companyCnpj": "0000000000",
        "branchCode": "000"
    },
]

def createOrGetAccountIfExists(**accountParams):
    account = MockedBankAccount.objects.filter(**accountParams).first()
    if account is None:
        account = MockedBankAccount.objects.create(**accountParams)

    return account

def populate():
    print("Populando novas contas bancárias aos usuários...")

    ricardo = User.objects.filter(email="ricardo@email.com").first()
    giuliana = User.objects.filter(email="giuliana@email.com").first()
    pedro = User.objects.filter(email="pedro@email.com").first()

    users = [ricardo, giuliana, pedro]
    for (itemIdx, item) in enumerate(BANK_DATA):
        for (userIdx, user) in enumerate(users):
            account = createOrGetAccountIfExists(
                brandName=item["branchName"],
                companyCnpj=item["companyCnpj"],
                branchCode =item["branchCode"],
                accountType=ACCOUNT_TYPES.CONTA_DEPOSITO_A_VISTA,
                number = f"000{itemIdx}{userIdx}",
                checkDigit = "0",
                accountid = "{itemIdx}{userIdx}",
            )

            if not user.accounts.filter(pk=account.pk).first():
                user.accounts.add(account)
