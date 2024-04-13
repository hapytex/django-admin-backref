# django-admin-backref

Generate admin URLs through the models.

This package automatically attaches an `.admin_links` object to all models with a registered `ModelAdmin` (for the default admin site).

This can then be used to generate the links both from the perspective of the *model object* as well as the model. One can then generate the path, or a link to that path with:

```python3
User.admin_links  # '/admin/auth/user/'
User.admin_links.add  # '/admin/auth/user/add'
User.admin_links.label  # '<a href="/admin/auth/user/">&lt;class &#x27;django.contrib.auth.models.User&#x27;&gt;</a>'
User(pk=1, username='username').admin_links  # '/admin/auth/user/1/change/'
User(pk=1, username='username').admin_links.delete  # '/admin/auth/user/1/delete/'
User(pk=1, username='username').admin_links.label  # '<a href="/admin/auth/user/1/change/">username</a>'
User(pk=1, username='username').admin_links.add  # '/admin/auth/user/add/'
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
    # …,
    'django_admin_backref',
]
```

Next all the models that have been registered for the *default* admin site, will automatically have a `.admin_links` attribute to access the admin URLs. If a model has already such attribute, for example because some other package, it will *not* override this.

## Usage

The `.admin_links` will generate an `AdminLink` object. For each view name, it then has attributes. We can access these in four ways:

 - <code>.<i>name</i></code>: the URL for the admin link with that name;
 - <code>.<i>name</i>_label</code>: a *safe* string that contains an `<a href="">` to that admin URL, and uses the label of the object;
 - <code>.get_<i>name</i>()</code>: the URL for the admin link with that name as a method; and
 - <code>.get_<i>name</i>_label()</code>: a *safe* string that contains an `<a href="">` to that admin URL, and uses the label of the object as a method.

For a simple model and for a simple admin, so without additional packages, for the class we have `.add`, `.changelist`, for *instances* it also contains `.change`, `.delete` and `.history`. Additional packages like `django-import-export` or special `ModelAdmin`s like the one for the `User` model introduce additional paths, like for example `.import` and `.password_change`.
