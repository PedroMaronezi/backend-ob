from django.db import models

from django.utils.translation import gettext_lazy as _

class ACCOUNT_TYPES(models.TextChoices):
    CONTA_DEPOSITO_A_VISTA = 'CONTA_DEPOSITO_A_VISTA', _ ('CONTA_DEPOSITO_A_VISTA')
    CONTA_POUPANCA = 'CONTA_POUPANCA', _('CONTA_POUPANCA')
    CONTA_PAGAMENTO_PRE_PAGA = 'CONTA_PAGAMENTO_PRE_PAGA', _('CONTA_PAGAMENTO_PRE_PAGA')

class MockedBankAccount(models.Model):

    def __str__(self):
        return f"{self.brandName}:{self.number}-{self.checkDigit}"

    brandName = models.CharField(max_length=255, default='', blank=False)
    companyCnpj = models.CharField(max_length=32, default='', blank=False)
    accountType = models.CharField(max_length=32, choices=ACCOUNT_TYPES.choices, default=ACCOUNT_TYPES.CONTA_DEPOSITO_A_VISTA, blank=False)
    # compeCode 
    branchCode = models.CharField(max_length=32, default='', blank=False)
    number = models.CharField(max_length=32, default='', blank=False)
    checkDigit = models.CharField(max_length=32, default='', blank=False)
    accountid = models.CharField(max_length=32, default='', blank=False)