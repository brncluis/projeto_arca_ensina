from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('dashboard', '0009_alter_conduta_id_alter_consulta_id_alter_medico_id_and_more'),
    ]
    operations = [
        migrations.CreateModel(
            name='Prescricao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_medicamento', models.CharField(max_length=100, verbose_name='Medicamento')),
                ('tipo_medicamento', models.CharField(max_length=100, blank=True, verbose_name='Tipo')),
                ('dose_calculada', models.CharField(max_length=100, verbose_name='Dose calculada')),
                ('unidade', models.CharField(max_length=50, blank=True, verbose_name='Unidade')),
                ('peso_utilizado', models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Peso (kg)')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescricoes', to='dashboard.paciente', verbose_name='Paciente')),
            ],
            options={'verbose_name': 'Prescrição', 'verbose_name_plural': 'Prescrições', 'ordering': ['-id']},
        ),
    ]