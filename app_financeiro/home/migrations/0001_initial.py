# Generated by Django 4.2.16 on 2024-10-18 17:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moneda_preferida', models.CharField(default='USD', max_length=10)),
                ('notificaciones_email', models.BooleanField(default=True)),
                ('tema', models.CharField(choices=[('light', 'Claro'), ('dark', 'Oscuro')], default='light', max_length=20)),
                ('idioma', models.CharField(choices=[('es', 'Español'), ('en', 'Inglés')], default='es', max_length=10)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
