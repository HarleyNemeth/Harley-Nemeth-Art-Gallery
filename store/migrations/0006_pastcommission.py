from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0005_commissionoffering"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="CommissionOffering",
            new_name="PastCommission",
        ),
        migrations.RenameField(
            model_name="pastcommission",
            old_name="is_active",
            new_name="is_visible",
        ),
        migrations.AlterModelOptions(
            name="pastcommission",
            options={
                "ordering": ["display_order", "title"],
                "verbose_name": "Past commission",
                "verbose_name_plural": "Past commissions",
            },
        ),
    ]
