from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistemas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='maratona',
            old_name='distancia_km',
            new_name='distancia',
        ),
        migrations.RemoveField(
            model_name='maratona',
            name='nome',
        ),
        migrations.AlterModelOptions(
            name='maratona',
            options={'ordering': ['data', 'cidade']},
        ),
    ]
