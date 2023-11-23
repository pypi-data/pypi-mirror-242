from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_user_phone"),
    ]

    operations = [
        migrations.RunSQL(
            """
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(98.30472222222222, 65.62972222222221), 4326) where name = 'Эвенкийский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(91.93944444444445, 53.325833333333335), 4326) where name = 'Шушенский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(89.2, 55.53333333333333), 4326) where name = 'Шарыповский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(94.5, 55.63333333333333), 4326) where name = 'Уярский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(89.98333333333333, 55.416666666666664), 4326) where name = 'Ужурский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(89.41666666666667, 56.68333333333333), 4326) where name = 'Тюхтетский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(88.0, 64.0), 4326) where name = 'Туруханский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(95.05, 57.233333333333334), 4326) where name = 'Тасеевский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(93.71527777777779, 71.91638888888889), 4326) where name = 'Таймырский Долгано-Ненецкий';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(93.28333333333333, 56.5), 4326) where name = 'Сухобузимский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(93.035, 60.38027777777778), 4326) where name = 'Северо-Енисейский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(94.89805555555556, 55.26), 4326) where name = 'Саянский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(94.7, 55.96666666666667), 4326) where name = 'Рыбинский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(92.26805555555555, 57.628055555555555), 4326) where name = 'Пировский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(94.38305555555554, 55.50111111111111), 4326) where name = 'Партизанский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(90.88333333333334, 55.0), 4326) where name = 'Новоселовский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(96.52111111111111, 56.20333333333333), 4326) where name = 'Нижнеингашский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(90.38333333333334, 56.0), 4326) where name = 'Назаровский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(94.68722222222223, 58.18666666666666), 4326) where name = 'Мотыгинский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(91.68333333333334, 53.7), 4326) where name = 'Минусинский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(93.76194444444444, 55.721111111111114), 4326) where name = 'Манский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(92.6725, 53.8975), 4326) where name = 'Курагинский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(91.56055555555555, 54.315), 4326) where name = 'Краснотуранский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(91.4, 56.166666666666664), 4326) where name = 'Козульский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(99.18333333333334, 58.68333333333333), 4326) where name = 'Кежемский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(92.86666666666666, 53.6), 4326) where name = 'Каратузский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(95.71666666666667, 56.2), 4326) where name = 'Канский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(93.27555555555556, 57.70333333333333), 4326) where name = 'Казачинский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(95.44611111111111, 55.64694444444444), 4326) where name = 'Ирбейский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(96.08305555555555, 56.0), 4326) where name = 'Иланский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(92.5, 54.5), 4326) where name = 'Идринский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(92.38333333333334, 53.18333333333333), 4326) where name = 'Ермаковский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(89.0, 60.0), 4326) where name = 'Енисейский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(92.45, 56.15), 4326) where name = 'Емельяновский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(95.22277777777778, 56.83083333333334), 4326) where name = 'Дзержинский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(90.75, 56.666666666666664), 4326) where name = 'Большеулуйский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(93.0, 57.0), 4326) where name = 'Большемуртинский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(97.5, 58.5), 4326) where name = 'Богучанский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(89.0, 56.0), 4326) where name = 'Боготольский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(90.75, 57.25), 4326) where name = 'Бирилюсский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(93.11444444444444, 56.02222222222222), 4326) where name = 'Березовский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(91.5, 55.5), 4326) where name = 'Балахтинский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(90.5, 56.25), 4326) where name = 'Ачинский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(96.0, 56.0), 4326) where name = 'Абанский';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(92.32638888888889, 56.23527777777778), 4326) where name = 'Кедровый';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(89.82555555555555, 55.28583333333333), 4326) where name = 'Солнечный';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(93.42750000000001, 56.121944444444445), 4326) where name = 'Подгорный';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(89.2, 55.525), 4326) where name = 'Шарыпово';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(93.36666666666666, 56.13333333333333), 4326) where name = 'Сосновоборск';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(88.21666666666667, 69.33333333333333), 4326) where name = 'Норильск';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(90.3913888888889, 56.006388888888885), 4326) where name = 'Назарово';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(91.68333333333334, 53.7), 4326) where name = 'Минусинск';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(92.48333333333333, 58.233333333333334), 4326) where name = 'Лесосибирск';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(95.7, 56.2), 4326) where name = 'Канск';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(94.58333333333333, 56.1), 4326) where name = 'Зеленогорск';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(93.53333333333333, 56.25), 4326) where name = 'Железногорск';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(92.13333333333334, 58.46666666666667), 4326) where name = 'Енисейск';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(92.38333333333334, 55.95), 4326) where name = 'Дивногорск';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(94.9, 55.9), 4326) where name = 'Бородино';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(89.51666666666667, 56.2), 4326) where name = 'Боготол';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(90.5, 56.266666666666666), 4326) where name = 'Ачинск';
update core_locality set gis_center = ST_SetSRID(ST_MakePoint(92.87138888888889, 56.011944444444445), 4326) where name = 'Красноярск';
"""
        )
    ]
