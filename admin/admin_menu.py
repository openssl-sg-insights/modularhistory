"""
ModularHistory's custom admin menu.

This custom admin menu is activated by the following line in settings.py:
    ADMIN_TOOLS_MENU = 'modularhistory.admin_menu.AdminMenu'
"""

from typing import Iterable

from admin_tools.menu import Menu, items
from django.apps import apps
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from admin.admin_site import admin_site

APPS_TO_INCLUDE = (
    'entities',
    'quotes',
    'occurrences',
    'sources',
    'images',
    'topics',
    'places',
    'staticpages',
    'account',
)


def _get_models_registered_in_app(app: str) -> Iterable:
    app_models = apps.get_app_config(app).get_models()
    return [model for model in app_models if model in admin_site.get_registry().keys()]


class AdminMenu(Menu):
    """Custom menu for ModularHistory's admin site."""

    apps_to_include = APPS_TO_INCLUDE

    class Media:
        """Static files to be included with the menu."""

        css = ()  # css = {'all': ('css/menu.css',)}
        js = ()  # js = ('js/menu.js',)

    def __init__(self, **kwargs):
        """Construct the admin menu."""
        super().__init__(**kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            items.Bookmarks(),
            items.AppList(
                title='Applications',
                exclude=['django.contrib.*', 'social_django.*', 'django_celery_*'],
            ),
        ] + self._menu_items

    @property
    def _menu_items(self):
        menu_items = []
        for app in self.apps_to_include:
            models = _get_models_registered_in_app(app)
            children = []
            for model_cls in models:
                model_name = model_cls.__name__
                children.append(
                    items.MenuItem(model_name, f'/admin/{app}/{model_name.lower()}/')
                )
            menu_items.append(items.MenuItem(app, children=children))
        return menu_items

    # def init_with_context(self, context):
    #     """Use this method if you need to access the request context."""
    #     super().init_with_context(context)
    #     Use sessions to store the visited pages stack
    #     history = request.session.get('modularhistory', [])
    #     for item in history:
    #         self.children.append(MenuItem(
    #             title=item['title'],
    #             url=item['url']
    #         ))
    #     # Add the current page to the history
    #     history.insert(0, {
    #         'title': context['title'],
    #         'url': request.META['PATH_INFO']
    #     })
    #     if len(history) > 10:
    #         history = history[:10]
    #     request.session['modularhistory'] = history
