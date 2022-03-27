# Generated by Django 4.0.2 on 2022-03-01 22:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MockedTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completedAuthorisedPaymentType', models.CharField(choices=[('TRANSACAO_EFETIVADA', 'Transação efetivada'), ('LANCAMENTO_FUTURO', 'Lançamento futuro')], default='LANCAMENTO_FUTURO', max_length=32)),
                ('creditDebitType', models.CharField(choices=[('CREDITO', 'Credito'), ('DEBITO', 'Débito')], default='CREDITO', max_length=32)),
                ('transactionName', models.CharField(default='', max_length=255)),
                ('transactionType', models.CharField(choices=[('TED', 'TED'), ('DOC', 'DOC'), ('PIX', 'PIX'), ('TRANSFERENCIA_MESMA_INSTITUICAO', 'TRANSFERENCIA_MESMA_INSTITUICAO'), ('BOLETO', 'BOLETO'), ('CONVENIO_ARRECADACAO', 'CONVENIO_ARRECADACAO'), ('PACOTE_TARIFA_SERVICOS', 'PACOTE_TARIFA_SERVICOS'), ('TARIFA_SERVICOS_AVULSOS', 'TARIFA_SERVICOS_AVULSOS'), ('FOLHA_PAGAMENTO', 'FOLHA_PAGAMENTO'), ('DEPOSITO', 'DEPOSITO'), ('SAQUE', 'SAQUE'), ('CARTAO', 'CARTAO'), ('ENCARGOS_JUROS_CHEQUE_ESPECIAL', 'ENCARGOS_JUROS_CHEQUE_ESPECIAL'), ('RENDIMENTO_APLIC_FINANCEIRA', 'RENDIMENTO_APLIC_FINANCEIRA'), ('PORTABILIDADE_SALARIO', 'PORTABILIDADE_SALARIO'), ('RESGATE_APLIC_FINANCEIRA', 'RESGATE_APLIC_FINANCEIRA'), ('OPERACAO_CREDITO', 'OPERACAO_CREDITO'), ('OUTROS', 'OUTROS')], default='OUTROS', max_length=32)),
                ('amount', models.FloatField(default=0)),
                ('transactionCurrency', models.CharField(default='BRL', max_length=32)),
                ('transactionDate', models.DateTimeField(default=datetime.datetime(2022, 3, 1, 22, 8, 48, 359784))),
                ('partieCnpjCpf', models.CharField(default='', max_length=32)),
                ('partiePersonType', models.CharField(choices=[('PESSOA_FISICA', 'Pessoa física - CPF'), ('PESSOA_JURIDICA', 'Pessoa jurídica - CNPF')], default='PESSOA_FISICA', max_length=32)),
                ('partieBranchCode', models.CharField(default='0', max_length=32)),
                ('partieNumber', models.CharField(default='0', max_length=32)),
                ('partieCheckDigit', models.CharField(default='0', max_length=32)),
            ],
        ),
    ]
