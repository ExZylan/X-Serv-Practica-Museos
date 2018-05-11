# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('comentario', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=128)),
                ('enlace', models.CharField(max_length=128)),
                ('descripcion', models.TextField()),
                ('accesible', models.IntegerField()),
                ('barrio', models.CharField(max_length=128)),
                ('distrito', models.CharField(max_length=128)),
                ('datos', models.CharField(max_length=128)),
                ('telefono', models.CharField(max_length=128)),
                ('direccion', models.CharField(max_length=128)),
                ('fax', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=128)),
                ('color', models.CharField(max_length=128)),
                ('fuente', models.IntegerField()),
                ('titulo', models.CharField(max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='favorito',
            name='museo',
            field=models.ForeignKey(to='museos.Museo'),
        ),
        migrations.AddField(
            model_name='favorito',
            name='usuario',
            field=models.ForeignKey(to='museos.Usuario'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='museo',
            field=models.ForeignKey(to='museos.Museo'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='usuario',
            field=models.ForeignKey(to='museos.Usuario'),
        ),
    ]
