# Importations
from django.urls import reverse

from wagtail.core import hooks
from wagtail.admin.menu import MenuItem

# Lien vers le site d'admin
class AdminMenuItem(MenuItem):
    # Méthodes
    def is_shown(self, request):
        return request.user.is_staff

@hooks.register('register_settings_menu_item')
def register_admin_site_menu_item():
    return AdminMenuItem('Administration', reverse('admin:index'), classnames='icon icon-cogs', order=850)
