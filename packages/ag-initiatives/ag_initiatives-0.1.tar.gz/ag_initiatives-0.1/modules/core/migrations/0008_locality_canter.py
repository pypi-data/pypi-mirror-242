from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_auto_20201008_1741"),
    ]

    operations = [
        migrations.RunSQL(
            """
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(93.43333333333334, 54.35), 4326) where name = 'Артёмовск';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(86.18333333333334, 69.4), 4326) where name = 'Дудинка';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(94.7, 55.96666666666667), 4326) where name = 'Заозёрный';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(86.56666666666666, 67.46666666666667), 4326) where name = 'Игарка';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(99.18333333333334, 58.6), 4326) where name = 'Кодинск';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(89.81666666666666, 55.31666666666667), 4326) where name = 'Ужур';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(94.31666666666666, 55.81666666666667), 4326) where name = 'Уяр';
"""
        )
    ]
