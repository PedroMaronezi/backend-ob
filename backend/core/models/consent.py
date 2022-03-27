from django.db import models
from datetime import datetime
from dateutil.relativedelta import relativedelta
from core.models import *

from django.utils.translation import gettext_lazy as _

class CONSENT_STATUS(models.TextChoices):
    AWAITING_AUTHORISATION = 'AGUARDANDO_AUTORIZACAO', _('Aguardando autorização')
    AUTHORIZED = 'AUTORIZADO', _('Autorizado')
    REVOKED = 'REVOGADO', _('Revogado')


class CONSENT_PERMISSION(models.TextChoices):
    ACCOUNTS_READ = 'LEITURA_DE_CONTA', _('Leitura de conta')
    ACCOUNTS_OVERDRAFT_LIMITS_READ = 'LEITURA_DE_CONTA_CHEQUE_ESPECIAL', _('Leitura de conta cheque especial')
    RESOURCES_READ = 'LEITURA_DE_RECURSOS', _('Leitura de recursos')

class CONSENT_OPTYPE(models.TextChoices):
    EDIT_PERMISSION = 'EDIT_PERMISSION', _('Editar permissão')
    RENOVATE = 'RENOVAR', _('Renovar')
    REVOKE = 'REVOGAR', _('Cancelar')



class OB_PERMISSION_VALUES(models.TextChoices):
    ACCOUNTS_READ = 'ACCOUNTS_READ', _('ACCOUNTS_READ')
    ACCOUNTS_BALANCES_READ = 'ACCOUNTS_BALANCES_READ', _('ACCOUNTS_BALANCES_READ')
    ACCOUNTS_TRANSACTIONS_READ = 'ACCOUNTS_TRANSACTIONS_READ', _('ACCOUNTS_TRANSACTIONS_READ')
    ACCOUNTS_OVERDRAFT_LIMITS_READ = 'ACCOUNTS_OVERDRAFT_LIMITS_READ', _('ACCOUNTS_OVERDRAFT_LIMITS_READ')
    CREDIT_CARDS_ACCOUNTS_READ = 'CREDIT_CARDS_ACCOUNTS_READ', _('CREDIT_CARDS_ACCOUNTS_READ')
    CREDIT_CARDS_ACCOUNTS_BILLS_READ = 'CREDIT_CARDS_ACCOUNTS_BILLS_READ', _('CREDIT_CARDS_ACCOUNTS_BILLS_READ')
    CREDIT_CARDS_ACCOUNTS_BILLS_TRANSACTIONS_READ = 'CREDIT_CARDS_ACCOUNTS_BILLS_TRANSACTIONS_READ', _('CREDIT_CARDS_ACCOUNTS_BILLS_TRANSACTIONS_READ')
    CREDIT_CARDS_ACCOUNTS_LIMITS_READ = 'CREDIT_CARDS_ACCOUNTS_LIMITS_READ', _('CREDIT_CARDS_ACCOUNTS_LIMITS_READ')
    CREDIT_CARDS_ACCOUNTS_TRANSACTIONS_READ = 'CREDIT_CARDS_ACCOUNTS_TRANSACTIONS_READ', _('CREDIT_CARDS_ACCOUNTS_TRANSACTIONS_READ')
    INVOICE_FINANCINGS_READ = 'INVOICE_FINANCINGS_READ', _('INVOICE_FINANCINGS_READ')
    INVOICE_FINANCINGS_PAYMENTS_READ = 'INVOICE_FINANCINGS_PAYMENTS_READ', _('INVOICE_FINANCINGS_PAYMENTS_READ')
    INVOICE_FINANCINGS_SCHEDULED_INSTALMENTS_READ = 'INVOICE_FINANCINGS_SCHEDULED_INSTALMENTS_READ', _('INVOICE_FINANCINGS_SCHEDULED_INSTALMENTS_READ')
    INVOICE_FINANCINGS_WARRANTIES_READ = 'INVOICE_FINANCINGS_WARRANTIES_READ', _('INVOICE_FINANCINGS_WARRANTIES_READ')
    FINANCINGS_READ = 'FINANCINGS_READ', _('FINANCINGS_READ')
    FINANCINGS_PAYMENTS_READ = 'FINANCINGS_PAYMENTS_READ', _('FINANCINGS_PAYMENTS_READ')
    FINANCINGS_SCHEDULED_INSTALMENTS_READ = 'FINANCINGS_SCHEDULED_INSTALMENTS_READ', _('FINANCINGS_SCHEDULED_INSTALMENTS_READ')
    FINANCINGS_WARRANTIES_READ = 'FINANCINGS_WARRANTIES_READ', _('FINANCINGS_WARRANTIES_READ')
    LOANS_READ = 'LOANS_READ', _('LOANS_READ')
    LOANS_PAYMENTS_READ = 'LOANS_PAYMENTS_READ', _('LOANS_PAYMENTS_READ')
    LOANS_SCHEDULED_INSTALMENTS_READ = 'LOANS_SCHEDULED_INSTALMENTS_READ', _('LOANS_SCHEDULED_INSTALMENTS_READ')
    LOANS_WARRANTIES_READ = 'LOANS_WARRANTIES_READ', _('LOANS_WARRANTIES_READ')
    UNARRANGED_ACCOUNTS_OVERDRAFT_READ = 'UNARRANGED_ACCOUNTS_OVERDRAFT_READ', _('UNARRANGED_ACCOUNTS_OVERDRAFT_READ')
    UNARRANGED_ACCOUNTS_OVERDRAFT_PAYMENTS_READ = 'UNARRANGED_ACCOUNTS_OVERDRAFT_PAYMENTS_READ', _('UNARRANGED_ACCOUNTS_OVERDRAFT_PAYMENTS_READ')
    UNARRANGED_ACCOUNTS_OVERDRAFT_SCHEDULED_INSTALMENTS_READ   = 'UNARRANGED_ACCOUNTS_OVERDRAFT_SCHEDULED_INSTALMENTS_READ  ', _('UNARRANGED_ACCOUNTS_OVERDRAFT_SCHEDULED_INSTALMENTS_READ  ')
    UNARRANGED_ACCOUNTS_OVERDRAFT_WARRANTIES_READ = 'UNARRANGED_ACCOUNTS_OVERDRAFT_WARRANTIES_READ', _('UNARRANGED_ACCOUNTS_OVERDRAFT_WARRANTIES_READ')
    RESOURCES_READ = 'RESOURCES_READ', _('RESOURCES_READ')  


class OBPermissions(models.Model):
    def __str__(self):
        return self.value

    value = models.CharField(max_length=64, choices=OB_PERMISSION_VALUES.choices, default=OB_PERMISSION_VALUES.ACCOUNTS_READ, blank=False)

# O formato destes objetos é de acordo com o response do "GET /consents/v1/consents/{consentId}"  definido em https://openbanking-brasil.github.io/areadesenvolvedor/?python#obter-detalhes-do-consentimento-identificado-por-consentid
# Mais uns dados bancários extras 
class MockedConsent(models.Model):
    consentId = models.CharField(max_length=64, unique=True, null=False, blank=False) #precisa ser um URN - exemplo:  "urn:bancoex:C1DD33123"
    creationDateTime = models.DateTimeField(null=False, default=datetime.now(), blank=False)
    status = models.CharField(max_length=255, choices=CONSENT_STATUS.choices, null=False, default=CONSENT_STATUS.AUTHORIZED, blank=False)
    statusUpdateDateTime = models.DateTimeField(null=False, default=datetime.now(),blank=False)
    permissions = models.ManyToManyField(OBPermissions, blank=False, default=None, null=True)
    expirationDateTime = models.DateTimeField(null=False, default=datetime.now() + relativedelta(months=2),blank=False) #validade de 2 meses
    transactionFromDateTime = models.DateTimeField(null=False, default=datetime.now() - relativedelta(years=1), blank=False) #só acessa os dados de até 1 ano atrás?
    transactionToDateTime = models.DateTimeField(null=False, default=datetime.now() + relativedelta(months=2), blank=False)
    user = models.ForeignKey(User, null=False, on_delete=models.DO_NOTHING)
    bankAccount = models.ForeignKey(MockedBankAccount, null=False, on_delete=models.DO_NOTHING)
