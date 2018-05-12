# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0002_remove_museo_datos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='fuente',
            new_name='tamano',
        ),
        migrations.AddField(
            model_name='usuario',
            name='fondo',
            field=models.CharField(default=8, max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='museo',
            name='direccion',
            field=models.CharField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombre',
            field=models.OneToOneField(related_name='usuario', to=settings.AUTH_USER_MODEL),
        ),
    ]
