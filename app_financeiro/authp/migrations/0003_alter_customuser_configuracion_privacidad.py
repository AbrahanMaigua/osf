# Generated by Django 4.2.16 on 2024-10-29 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authp', '0002_customuser_consentimiento_datos_setting_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='configuracion_privacidad',
            field=models.BooleanField(default=False),
        ),
    ]