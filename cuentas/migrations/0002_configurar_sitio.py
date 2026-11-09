from django.db import migrations


def configurar_sitio(apps, schema_editor):
    """Pone el nombre 'AgroValle' al sitio, que aparece en los correos de allauth."""
    Site = apps.get_model('sites', 'Site')
    Site.objects.update_or_create(
        id=1,
        defaults={'domain': '127.0.0.1:8000', 'name': 'AgroValle'},
    )


class Migration(migrations.Migration):

    dependencies = [
        ('cuentas', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(configurar_sitio, migrations.RunPython.noop),
    ]
