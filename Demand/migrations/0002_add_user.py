# Generated to add user FK after CustomerUser migration
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Demand', '0001_initial'),
        ('CustomerUser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='demand_has_user', to='CustomerUser.customeruser'),
        ),
    ]
