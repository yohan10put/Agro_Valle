from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from allauth.account.models import EmailAddress

from .models import Perfil
from .permisos import NOMBRE_GRUPO_TECNICOS

Usuario = get_user_model()


class RegistroTests(TestCase):
    def setUp(self):
        # allauth limita los correos repetidos usando la caché; se limpia entre pruebas.
        cache.clear()

    def datos(self, **cambios):
        datos = {
            'email': 'juan@ejemplo.com',
            'password1': 'ClaveSegura.2026',
            'password2': 'ClaveSegura.2026',
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'telefono': '70000000',
            'comunidad': 'Guadalupe',
            'rol': 'productor',
        }
        datos.update(cambios)
        return datos

    def test_registro_crea_productor_y_envia_verificacion(self):
        self.client.post(reverse('account_signup'), self.datos())
        usuario = Usuario.objects.get(email='juan@ejemplo.com')
        self.assertEqual(usuario.perfil.rol, Perfil.Rol.PRODUCTOR)
        self.assertEqual(usuario.perfil.comunidad, 'Guadalupe')
        self.assertFalse(usuario.is_staff)
        self.assertFalse(EmailAddress.objects.get(user=usuario).verified)
        self.assertEqual(len(mail.outbox), 1)

    def test_no_se_puede_registrar_como_tecnico(self):
        self.client.post(reverse('account_signup'), self.datos(rol='tecnico'))
        self.assertFalse(Usuario.objects.filter(email='juan@ejemplo.com').exists())

    def test_productor_debe_indicar_comunidad(self):
        self.client.post(reverse('account_signup'), self.datos(comunidad=''))
        self.assertFalse(Usuario.objects.filter(email='juan@ejemplo.com').exists())

    def test_comprador_sin_comunidad(self):
        self.client.post(reverse('account_signup'), self.datos(rol='comprador', comunidad=''))
        usuario = Usuario.objects.get(email='juan@ejemplo.com')
        self.assertEqual(usuario.perfil.rol, Perfil.Rol.COMPRADOR)


class TecnicoTests(TestCase):
    def setUp(self):
        cache.clear()
        self.admin = Usuario.objects.create_superuser('admin', 'admin@ejemplo.com', 'ClaveSegura.2026')

    def test_admin_registra_tecnico(self):
        self.client.force_login(self.admin)
        self.client.post(reverse('nuevo_tecnico'), {
            'first_name': 'Ana',
            'last_name': 'Rojas',
            'email': 'Ana@Ejemplo.com',
            'telefono': '71111111',
        })
        tecnico = Usuario.objects.get(email='ana@ejemplo.com')
        self.assertEqual(tecnico.perfil.rol, Perfil.Rol.TECNICO)
        self.assertTrue(tecnico.is_staff)
        self.assertFalse(tecnico.is_superuser)
        self.assertTrue(tecnico.groups.filter(name=NOMBRE_GRUPO_TECNICOS).exists())
        self.assertTrue(EmailAddress.objects.get(user=tecnico).verified)
        # Correo de bienvenida + correo para crear la contraseña
        self.assertEqual(len(mail.outbox), 2)

    def test_grupo_tecnicos_solo_tiene_permisos_de_cultivos(self):
        self.client.force_login(self.admin)
        self.client.post(reverse('nuevo_tecnico'), {
            'first_name': 'Ana', 'last_name': 'Rojas', 'email': 'ana@ejemplo.com',
        })
        tecnico = Usuario.objects.get(email='ana@ejemplo.com')
        apps = {p.split('.')[0] for p in tecnico.get_all_permissions()}
        self.assertEqual(apps, {'cultivos'})

    def test_correo_repetido_no_se_registra(self):
        self.client.force_login(self.admin)
        respuesta = self.client.post(reverse('nuevo_tecnico'), {
            'first_name': 'Otro', 'last_name': 'Admin', 'email': 'admin@ejemplo.com',
        })
        self.assertContains(respuesta, 'Ya existe una cuenta con este correo.')

    def test_solo_el_administrador_registra_tecnicos(self):
        productor = Usuario.objects.create_user('p', 'p@ejemplo.com', 'ClaveSegura.2026')
        self.client.force_login(productor)
        respuesta = self.client.get(reverse('nuevo_tecnico'))
        self.assertEqual(respuesta.status_code, 302)

    def test_tecnico_va_al_panel_al_iniciar(self):
        tecnico = Usuario.objects.create_user('t', 't@ejemplo.com', 'ClaveSegura.2026')
        tecnico.perfil.rol = Perfil.Rol.TECNICO
        tecnico.perfil.save()
        self.client.force_login(tecnico)
        respuesta = self.client.get(reverse('inicio'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, 'cuentas/inicio_tecnico.html')

    def test_cambiar_rol_quita_el_panel(self):
        usuario = Usuario.objects.create_user('t', 't@ejemplo.com', 'ClaveSegura.2026')
        usuario.perfil.rol = Perfil.Rol.TECNICO
        usuario.perfil.save()
        usuario.perfil.rol = Perfil.Rol.PRODUCTOR
        usuario.perfil.save()
        usuario.refresh_from_db()
        self.assertFalse(usuario.is_staff)
        self.assertFalse(usuario.groups.exists())
