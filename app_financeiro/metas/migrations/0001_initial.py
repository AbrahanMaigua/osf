# Generated by Django 4.2.16 on 2024-10-30 17:37

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
            name='MetaAhorro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('objetivo_monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('monto_ahorrado', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('fecha_inicio', models.DateField(auto_now_add=True)),
                ('fecha_limite', models.DateField(blank=True, null=True)),
                ('descripcion', models.TextField(blank=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]