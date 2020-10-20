from django.urls import path

from admin import SearchableModelAdmin, TabularInline, admin_site
from entities.views import AttributeeSearchView
from sources import models
from sources.admin.filters import (
    AttributeeFilter,
    HasContainerFilter,
    HasFileFilter,
    HasFilePageOffsetFilter,
    HasPageNumber,
    ImpreciseDateFilter,
    TypeFilter
)
from sources.admin.source_inlines import (
    AttributeesInline,
    ContainedSourcesInline,
    ContainersInline,
    RelatedInline
)


class SourceAdmin(SearchableModelAdmin):
    """Admin for sources."""

    model = models.Source
    list_display = [
        'pk',
        'html',
        'date_string',
        'location',
        'admin_source_link',
        'type'
    ]
    list_filter = [
        'verified',
        HasContainerFilter,
        HasFileFilter,
        HasFilePageOffsetFilter,
        HasPageNumber,
        ImpreciseDateFilter,
        'hidden',
        AttributeeFilter,
        TypeFilter
    ]
    readonly_fields = SearchableModelAdmin.readonly_fields + ['db_string']
    search_fields = models.Source.searchable_fields
    ordering = ['date', 'db_string']
    inlines = [AttributeesInline, ContainersInline, ContainedSourcesInline, RelatedInline]
    autocomplete_fields = ['db_file', 'location']

    # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.date_hierarchy
    date_hierarchy = 'date'

    # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_per_page
    list_per_page = 10

    # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_as
    save_as = True

    # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_as_continue
    save_as_continue = True

    def get_queryset(self, request):
        """
        Return the queryset of quotes to be displayed in the admin.

        https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_queryset
        """
        qs = models.Source.objects.all().select_related(
            'db_file',
            'location',
            'publication',
            'collection',
            'collection__repository'
        )
        ordering = self.get_ordering(request)
        if ordering and ordering != models.Source.get_meta().ordering:
            qs = qs.order_by(*ordering)
        return qs

    def get_fields(self, request, model_instance=None):
        """Returns reordered fields to be displayed in the admin."""
        fields = list(super().get_fields(request, model_instance))
        if 'database_string' in fields:
            fields.remove('database_string')
            fields.insert(0, 'database_string')
        return fields

    def get_urls(self):
        """TODO: add docstring."""
        urls = super().get_urls()
        additional_urls = [
            path(
                'attributee_search/',
                self.admin_site.admin_view(AttributeeSearchView.as_view(model_admin=self)),
                name='attributee_search'
            ),
        ]
        return additional_urls + urls


class SpeechAdmin(SourceAdmin):
    """TODO: add docstring."""

    list_display = ['string', 'location', 'date_string']
    search_fields = ['db_string', 'location__name']


class SourcesInline(TabularInline):
    """TODO: add docstring."""

    model = models.Source
    extra = 0
    fields = ['verified', 'hidden', 'date_is_circa', 'creators', 'url', 'date', 'publication_date']


admin_site.register(models.Source, SourceAdmin)
admin_site.register(models.Speech, SpeechAdmin)
admin_site.register(models.Interview, SpeechAdmin)
