# Generated by Django 3.2.23 on 2024-02-03 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0007_remove_expediente_notas_personales'),
        ('psicologo', '0011_psicologo_solicitudescita'),
        ('evento', '0004_evento_motivo'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudAgenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('titulo', models.CharField(max_length=255)),
                ('motivo', models.CharField(blank=True, max_length=1000, null=True)),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paciente.paciente', verbose_name='Paciente')),
                ('psicologo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psicologo.psicologo', verbose_name='Psicologo')),
            ],
        ),
    ]