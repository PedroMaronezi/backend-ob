from rest_framework import serializers
from core.models import MockedTransactions, MockedBankAccount, User, MockedConsent, Category, OBPermissions


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ChangeAccountInfoSerializer(serializers.Serializer):
    model = User

    password = serializers.CharField(required=True)
    new_name = serializers.CharField(required=False)
    new_email = serializers.CharField(required=False)
    new_tel = serializers.CharField(required=False)

class CategorySerializer(serializers.ModelSerializer):
    # pk = serializers.IntegerField(source='pk')
    class Meta:
        model = Category
        fields = ('pk', 'readableText',)

class TransactionsSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='transactionType')
    category = CategorySerializer()
    class Meta:
        model = MockedTransactions
        fields = ('completedAuthorisedPaymentType', 'creditDebitType', 'transactionName', 'type', 'amount', 'transactionCurrency', 'transactionDate', 'partieCnpjCpf', 'partiePersonType', 'partieBranchCode', 'partieNumber', 'partieCheckDigit', 'category')

class BankAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = MockedBankAccount
        fields = ('brandName', 'companyCnpj', 'accountType', 'branchCode', 'number', 'checkDigit', 'accountid',)

class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OBPermissions
        fields = ('value',)

class ConsentSerializer(serializers.ModelSerializer):

    bankAccount = BankAccountSerializer()
    permissions = PermissionsSerializer(many=True)
    class Meta:
        model = MockedConsent
        fields = ('consentId','creationDateTime','status','statusUpdateDateTime','permissions','expirationDateTime','transactionFromDateTime','transactionToDateTime','user','bankAccount',)

