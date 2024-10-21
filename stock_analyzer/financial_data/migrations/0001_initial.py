# Generated by Django 5.1.2 on 2024-10-19 21:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FinancialData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('open_price', models.FloatField()),
                ('close_price', models.FloatField()),
                ('high_price', models.FloatField()),
                ('low_price', models.FloatField()),
                ('volume', models.BigIntegerField()),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financial_data.symbol')),
            ],
            options={
                'indexes': [models.Index(fields=['symbol', 'date'], name='financial_d_symbol__43a583_idx')],
                'unique_together': {('symbol', 'date')},
            },
        ),
    ]
