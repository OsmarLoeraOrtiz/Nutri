from django.contrib.auth.mixins import UserPassesTestMixin

#Verifica que el usuario este en el grupo 'Usiarios Registrados' para restringir las funcionalidades del egistro.
class UsuarioRegistradoRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='Usuario-Registrado').exists()