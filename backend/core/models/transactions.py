from django.db import models
from datetime import datetime

from django.utils.translation import gettext_lazy as _

from core.models.category import Category

class COMPLETED_AUTHORIZED_PAYMENT_TYPE(models.TextChoices):
    TRANSACAO_EFETIVADA = 'TRANSACAO_EFETIVADA', _('Transação efetivada')
    LANCAMENTO_FUTURO = 'LANCAMENTO_FUTURO', _('Lançamento futuro')

class CREDIT_DEBIT_TYPE(models.TextChoices):
    CREDITO = 'CREDITO', _('Credito')
    DEBITO = 'DEBITO', _('Débito')

class TRANSACTION_TYPE(models.TextChoices):
    TED = 'TED', _('TED')
    DOC = 'DOC', _('DOC')
    PIX = 'PIX', _('PIX')
    TRANSFERENCIA_MESMA_INSTITUICAO = 'TRANSFERENCIA_MESMA_INSTITUICAO', _('TRANSFERENCIA_MESMA_INSTITUICAO')
    BOLETO = 'BOLETO', _('BOLETO')
    CONVENIO_ARRECADACAO = 'CONVENIO_ARRECADACAO', _('CONVENIO_ARRECADACAO')
    PACOTE_TARIFA_SERVICOS = 'PACOTE_TARIFA_SERVICOS', _('PACOTE_TARIFA_SERVICOS')
    TARIFA_SERVICOS_AVULSOS = 'TARIFA_SERVICOS_AVULSOS', _('TARIFA_SERVICOS_AVULSOS')
    FOLHA_PAGAMENTO = 'FOLHA_PAGAMENTO', _('FOLHA_PAGAMENTO')
    DEPOSITO = 'DEPOSITO', _('DEPOSITO')
    SAQUE = 'SAQUE', _('SAQUE')
    CARTAO = 'CARTAO', _('CARTAO')
    ENCARGOS_JUROS_CHEQUE_ESPECIAL = 'ENCARGOS_JUROS_CHEQUE_ESPECIAL', _('ENCARGOS_JUROS_CHEQUE_ESPECIAL')
    RENDIMENTO_APLIC_FINANCEIRA = 'RENDIMENTO_APLIC_FINANCEIRA', _('RENDIMENTO_APLIC_FINANCEIRA')
    PORTABILIDADE_SALARIO = 'PORTABILIDADE_SALARIO', _('PORTABILIDADE_SALARIO')
    RESGATE_APLIC_FINANCEIRA = 'RESGATE_APLIC_FINANCEIRA', _('RESGATE_APLIC_FINANCEIRA')
    OPERACAO_CREDITO = 'OPERACAO_CREDITO', _('OPERACAO_CREDITO')
    OUTROS = 'OUTROS', _('OUTROS')

class PARTIE_CNPJ_CPF_TYPE(models.TextChoices):
    PESSOA_FISICA= 'PESSOA_FISICA', _('Pessoa física - CPF')
    PESSOA_JURIDICA = 'PESSOA_JURIDICA', _('Pessoa jurídica - CNPF')


# O formato destes objetos é de acordo com o AccountTransactionsData definido em https://openbanking-brasil.github.io/areadesenvolvedor/#tocS_AccountTransactionsData
class MockedTransactions(models.Model):
    completedAuthorisedPaymentType = models.CharField(max_length=32, choices=COMPLETED_AUTHORIZED_PAYMENT_TYPE.choices, default=COMPLETED_AUTHORIZED_PAYMENT_TYPE.LANCAMENTO_FUTURO, null=False, blank=False)
    creditDebitType = models.CharField(max_length=32, choices=CREDIT_DEBIT_TYPE.choices, default=CREDIT_DEBIT_TYPE.CREDITO, null=False, blank=False)
    transactionName = models.CharField(max_length=255, null=False, default="", blank=False)
    transactionType = models.CharField(max_length=32, choices=TRANSACTION_TYPE.choices, default=TRANSACTION_TYPE.OUTROS, null=False, blank=False) # campo "type" na documentação. Verificar se o nome foi mapeado corretamente no serializer
    amount = models.FloatField(null=False, default=0, blank=False)
    transactionCurrency = models.CharField(max_length=32, default= 'BRL', null=False, blank=False)
    transactionDate = models.DateTimeField(null=False, default=datetime.now(), blank=False)
    partieCnpjCpf = models.CharField(max_length=32, null=False, default='', blank=False)
    partiePersonType = models.CharField(max_length=32, choices=PARTIE_CNPJ_CPF_TYPE.choices, default=PARTIE_CNPJ_CPF_TYPE.PESSOA_FISICA, blank=False)
    # partieCompeCode Não entendi bem o que é -> Confirmar e adicionar campo
    partieBranchCode = models.CharField(max_length=32, default='0', blank=False)
    partieNumber = models.CharField(max_length=32, default='0', blank=False)
    partieCheckDigit = models.CharField(max_length=32, default='0', blank=False)
    category = models.ForeignKey(Category, default=None, blank=False, on_delete=models.SET_DEFAULT)

