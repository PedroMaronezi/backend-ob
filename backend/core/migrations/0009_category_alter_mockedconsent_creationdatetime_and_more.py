# Generated by Django 4.0.2 on 2022-03-16 01:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_mockedconsent_creationdatetime_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('readableText', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='mockedconsent',
            name='creationDateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 16, 1, 57, 16, 397712)),
        ),
        migrations.AlterField(
            model_name='mockedconsent',
            name='expirationDateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 16, 1, 57, 16, 397823)),
        ),
        migrations.AlterField(
            model_name='mockedconsent',
            name='statusUpdateDateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 16, 1, 57, 16, 397782)),
        ),
        migrations.AlterField(
            model_name='mockedconsent',
            name='transactionFromDateTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 16, 1, 57, 16, 397889)),
        ),
        migrations.AlterField(
            model_name='mockedconsent',
            name='transactionToDateTime',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 16, 1, 57, 16, 397944)),
        ),
        migrations.AlterField(
            model_name='mockedtransactions',
            name='transactionDate',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 16, 1, 57, 16, 393514)),
        ),
        migrations.AddField(
            model_name='mockedtransactions',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='core.category'),
        ),
    ]