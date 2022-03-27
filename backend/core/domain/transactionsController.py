from core.models import MockedBankAccount, MockedTransactions, Category
from core.models.transactions import CREDIT_DEBIT_TYPE
from core.serializers import CategorySerializer, TransactionsSerializer, BankAccountSerializer


def getUserTransactions(user, filterParams):
    # As seguintes listas de banco e de conta são simplificadas pois estas listagens dependem da implementação da parte de Consentimentos
    accounts = user.accounts.all()
    
    transactions = MockedTransactions.objects.none()
    for account in accounts:
        accountTransactions = MockedTransactions.objects.filter(
            partieNumber=account.number,
            partieCheckDigit=account.checkDigit,
            partieBranchCode=account.branchCode
        )
        if (filterParams and "credit_type" in filterParams):
            if filterParams["credit_type"] == CREDIT_DEBIT_TYPE.DEBITO:
                accountTransactions = accountTransactions.filter(creditDebitType=CREDIT_DEBIT_TYPE.DEBITO)
            elif filterParams["credit_type"] == CREDIT_DEBIT_TYPE.CREDITO:
                accountTransactions = accountTransactions.filter(creditDebitType=CREDIT_DEBIT_TYPE.CREDITO)
        
        transactions = transactions | accountTransactions
        
    transactions = transactions.order_by('-transactionDate')
    return transactions

def separateTransactionsByYear(transactions):
    years = []
    for transaction in transactions:
        if transaction.transactionDate.year not in years:
            years.append(transaction.transactionDate.year)

    separatedTransactions = []
    for year in years:
        yearlyTransactions = []
        for transaction in transactions:
            if transaction.transactionDate.year == year:
                yearlyTransactions.append(transaction)
        
        separatedTransactions.append({
            "year": year,
            "transactions": yearlyTransactions
        })
        
    # Ordena os objetos de acordo com o ano
    separatedTransactions.sort(key=lambda x: x["year"], reverse=True)
    
    return separatedTransactions

def separateTransactionsByMonth(transactions):
    yearlyTransactions = separateTransactionsByYear(transactions)

    separatedTransactions = []
    for yearObject in yearlyTransactions:
        months = []
        for transaction in yearObject["transactions"]:
            if transaction.transactionDate.month not in months:
                months.append(transaction.transactionDate.month)
        
        auxObj = []
        for month in months:
            monthlyTransactions = []
            for transaction in transactions:
                if transaction.transactionDate.month == month:
                    monthlyTransactions.append(transaction)
        
            auxObj.append({
                "year": yearObject["year"],
                "month": month,
                "transactions": monthlyTransactions
            })
        
        # Ordena os objetos de acordo com o mês
        auxObj.sort(key=lambda x: x["month"], reverse=True)
        for item in auxObj:
            separatedTransactions.append(item)

    return separatedTransactions

def getTransactionsQuerysetBalance(transactions):
    balance = 0
    debit = 0
    credit = 0
    for transaction in transactions:
        amount = float(transaction.amount) 
        
        if transaction.creditDebitType == CREDIT_DEBIT_TYPE.DEBITO:
            debit += amount
            amount = -amount
        else:
            credit += amount
        balance += amount

    return (round(balance, 2), round(debit, 2),round(credit, 2))

def getUserBalance(user, filterParams):
    if ('by' in filterParams):
        if filterParams["by"] == "account": 
            userTransactions = getUserTransactions(user, None)
            userTransactionsObject = formatTransactionsByAccount(userTransactions, False)

            auxArray =[]
            for accountData in userTransactionsObject:
                auxArray.append({
                    "account": accountData["account"],
                    "transactionsByMonth": separateTransactionsByMonth(accountData["transactions"])
                })
            
            monthlyBalanceObject = []
            for accountData in auxArray:
                monthlyBalance = []
                for monthlyTransactionsObject in accountData["transactionsByMonth"]:
                    (balanceData, debitData,  creditData) = getTransactionsQuerysetBalance(monthlyTransactionsObject["transactions"])
                    monthlyBalance.append({
                        "year":monthlyTransactionsObject["year"],
                        "month":monthlyTransactionsObject["month"],
                        "balance": balanceData,
                        "debit": debitData,
                        "credit": creditData
                    })
                monthlyBalanceObject.append({
                    "account": BankAccountSerializer(accountData["account"]).data,
                    "balance": monthlyBalance
                })
            
            return monthlyBalanceObject
        elif filterParams["by"] == "category":
            return getUserBalanceByCategories(user)
    else :
        userTransactions = getUserTransactions(user, None)

        transactionsByMonth = separateTransactionsByMonth(userTransactions)

        monthlyBalance = []
        for monthlyTransactionsObject in transactionsByMonth:
            (balanceData, debitData,  creditData) = getTransactionsQuerysetBalance(monthlyTransactionsObject["transactions"])
            monthlyBalance.append({
                "year":monthlyTransactionsObject["year"],
                "month":monthlyTransactionsObject["month"],
                "balance": balanceData,
                "debit": debitData,
                "credit": creditData
            })
        
        return monthlyBalance

def getUserBalanceByCategories(user):
    categoriesPks = []
    userTransactions = getUserTransactions(user, None)

    for transaction in userTransactions:
        if transaction.category.pk not in categoriesPks:
            categoriesPks.append(transaction.category.pk)
    
    categoriesPks.sort()

    balanceByCategories = []
    for categoryPk in categoriesPks:
        category = Category.objects.filter(pk=categoryPk).first()
        transactions = userTransactions.filter(category=category)

        transactionsByMonth = separateTransactionsByMonth(transactions)

        monthlyBalance = []
        for monthlyTransactionsObject in transactionsByMonth:
            (balanceData, debitData,  creditData) = getTransactionsQuerysetBalance(monthlyTransactionsObject["transactions"])
            monthlyBalance.append({
                "year":monthlyTransactionsObject["year"],
                "month":monthlyTransactionsObject["month"],
                "balance": balanceData,
                "debit": debitData,
                "credit": creditData
            })
        
        balanceByCategories.append({
            "category": CategorySerializer(category).data,
            "balanceData": monthlyBalance
        })
    
    return balanceByCategories


def formatTransactionsByAccount(userTransactions, returnSerialized=True):
    accountCodes = []
    for transaction in userTransactions:
        if transaction.partieBranchCode not in accountCodes:
            accountCodes.append(transaction.partieBranchCode)

    data = []
    for accountCode in accountCodes:
        accountTransactions = userTransactions.filter(partieBranchCode=accountCode)
        account = MockedBankAccount.objects.filter(branchCode=accountCode).first()

        if (returnSerialized):
            data.append({
                "account": BankAccountSerializer(account).data,
                "transactions": TransactionsSerializer(accountTransactions, many=True).data
            })
        else: 
            data.append({
                "account": account,
                "transactions": accountTransactions
            })
    return data
