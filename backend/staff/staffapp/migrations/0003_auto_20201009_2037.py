# Generated by Django 3.1.2 on 2020-10-09 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffapp', '0002_auto_20201007_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupation',
            name='fire_date',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='occupation',
            name='hire_date',
            field=models.CharField(max_length=200),
        ),
    ]
