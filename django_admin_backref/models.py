from functools import partial

from django.urls import reverse
from django.db import models
from django.utils.html import format_html


class AdminLink:
    instance = None
    default_admin_link = "changelist"

    def __init__(self, model):
        self.model = model
        from django.contrib.admin import site

        self.modeladmin = modeladmin = site._registry.get(model)
        if modeladmin is None:
            raise AttributeError("The model has no ModelAdmin attached to it.")

    def __dir__(self):
        include_object_id = self.instance is not None
        model_prefix = self.model_prefix
        nprefix = len(model_prefix)
        extras = list(super().__dir__())
        for url in self.modeladmin.urls:
            print((include_object_id, url.name))
            if (
                url.name
                and url.name.startswith(model_prefix)
                and (include_object_id or not url.pattern.converters)
            ):
                base_name = url.name[nprefix:]
                extras.append(base_name)
                extras.append(f"get_{base_name}")
                extras.append(f"{base_name}_label")
                extras.append(f"get_{base_name}_label")
        return extras

    def generate_label(self, item):
        try:
            item.generate_label()
        except AttributeError:
            try:
                return str(item)
            except:
                return ""

    @property
    def label(self):
        return self.reverse(
            self.default_admin_link,
            label=self.generate_label(self.instance or self.model),
        )

    @property
    def model_prefix(self):
        return f"{self.model._meta.app_label}_{self.model._meta.model_name}_"

    @property
    def prefix(self):
        return f"admin:{self.model_prefix}"

    def reverse(self, action, *args, label=None, **kwargs):
        url = reverse(f"{self.prefix}{action}", args=args, kwargs=kwargs)
        if label is not None:
            return format_html('<a href="{}">{}</a>', url, label)
        return url

    def __str__(self):
        return self.reverse(self.default_admin_link)

    def __repr__(self):
        return str(self)

    def __getattr__(self, item):
        if item.endswith("_label"):
            label = self.generate_label(self.instance or self.model)
            item = item[:-6]
        else:
            label = None
        if item.startswith("get_"):
            return partial(self.reverse, item[4:], label=label)
        else:
            return self.reverse(item, label=label)


class AdminObjectLink(AdminLink):
    default_admin_link = "change"

    def __init__(self, instance):
        super().__init__(type(instance))
        self.instance = instance

    def reverse(self, action, *args, **kwargs):
        try:
            return super().reverse(action, self.instance.pk, *args, **kwargs)
        except:
            return super().reverse(action, **kwargs)


class AdminSiteLinks:
    def __get__(self, obj, obj_type=None):
        if obj is not None:
            return AdminObjectLink(obj)
        else:
            return AdminLink(obj_type)


class AdminRegistredModel(models.Model):
    admin_links = AdminSiteLinks()

    class Meta:
        abstract = True
