# Generated by Django 4.2.1 on 2023-05-31 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_payment_orderplaced'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(choices=[('Принят', 'Принят'), ('Упакован', 'Упакован'), ('В пути', 'В пути'), ('Доставлен', 'Доставлен'), ('Отмена', 'Отмена'), ('В ожидании', 'В ожиданнии')], default='Pending', max_length=50),
        ),
    ]