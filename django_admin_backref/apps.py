from django.apps import AppConfig


class DjangoAdminBackrefConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_admin_backref"

    def ready(self):
        from django.contrib.admin import site
        from .models import AdminSiteLinks

        try:
            registry = site._registry
        except LookupError:
            registry = ()

        for model in registry:
            if not hasattr(model, "admin_links"):
                model.admin_links = AdminSiteLinks()
