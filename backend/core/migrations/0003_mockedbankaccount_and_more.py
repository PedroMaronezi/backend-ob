# Generated by Django 4.0.2 on 2022-03-01 23:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_mockedtransactions'),
    ]

    operations = [
        migrations.CreateModel(
            name='MockedBankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brandName', models.CharField(default='', max_length=255)),
                ('companyCnpj', models.CharField(default='', max_length=32)),
                ('accountType', models.CharField(choices=[('CONTA_DEPOSITO_A_VISTA', 'CONTA_DEPOSITO_A_VISTA'), ('CONTA_POUPANCA', 'CONTA_POUPANCA'), ('CONTA_PAGAMENTO_PRE_PAGA', 'CONTA_PAGAMENTO_PRE_PAGA')], default='CONTA_DEPOSITO_A_VISTA', max_length=32)),
                ('branchCode', models.CharField(default='', max_length=32)),
                ('number', models.CharField(default='', max_length=32)),
                ('checkDigit', models.CharField(default='', max_length=32)),
                ('accountid', models.CharField(default='', max_length=32)),
            ],
        ),
        migrations.AlterField(
            model_name='mockedtransactions',
            name='transactionDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 1, 23, 7, 48, 625387)),
        ),
    ]
