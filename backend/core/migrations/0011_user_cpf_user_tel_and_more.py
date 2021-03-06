# Generated by Django 4.0.2 on 2022-03-21 23:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_mockedconsent_bankaccount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cpf',
            field=models.CharField(max_length=14, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='tel',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='mockedconsent',
            name='creationDateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 21, 20, 11, 29, 428311)),
        ),
        migrations.AlterField(
            model_name='mockedconsent',
            name='expirationDateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 21, 20, 11, 29, 428311)),
        ),
        migrations.AlterField(
            model_name='mockedconsent',
            name='statusUpdateDateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 21, 20, 11, 29, 428311)),
        ),
        migrations.AlterField(
            model_name='mockedconsent',
            name='transactionFromDateTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 21, 20, 11, 29, 428311)),
        ),
        migrations.AlterField(
            model_name='mockedconsent',
            name='transactionToDateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 21, 20, 11, 29, 428311)),
        ),
        migrations.AlterField(
            model_name='mockedtransactions',
            name='transactionDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 21, 20, 11, 29, 414348)),
        ),
    ]
