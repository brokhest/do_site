# Generated by Django 4.0 on 2022-01-25 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_file_name_alter_file_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]