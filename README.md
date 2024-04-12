# django-admin-backref

Generate admin URLs through the models.

This package automatically attaches an `.admin_links` object to all models with a registered `ModelAdmin` (for the default admin site).

This can then be used to generate the links both from the perspective of the *model object* as well as the model. One can then generate the path, or a link to that path with:

```
User.admin_links.add  # /admin/auth/user/add
```

## Installation

You install the package with:

```bash
pip install django-admin-backref
```

Next you can add the `django_admin_backref` to the `INSTALLED_APPS`:

```python3
# settings.py

INSTALLED_APPS = [
    # 
]
```