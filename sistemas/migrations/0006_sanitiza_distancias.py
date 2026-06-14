from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistemas', '0005_maratona_criado_por'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                UPDATE sistemas_maratona
                SET distancia = CASE
                    WHEN CAST(distancia AS REAL) < 0.01 THEN 0.01
                    WHEN CAST(distancia AS REAL) > 999.99 THEN 999.99
                    ELSE ROUND(CAST(distancia AS REAL), 2)
                END
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
