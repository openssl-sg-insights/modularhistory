from django.urls import path

from admin import SearchableModelAdmin, TabularInline, admin_site
from entities.views import EntitySearchView
from sources import models
from sources.admin.filters import (
    AttributeeFilter,
    HasContainerFilter,
    HasFileFilter,
    HasFilePageOffsetFilter,
    ImpreciseDateFilter,
    TypeFilter,
)
from sources.admin.source_inlines import (
    AttributeesInline,
    ContainedSourcesInline,
    ContainersInline,
    RelatedInline,
)


class SourceAdmin(SearchableModelAdmin):
    """Admin for sources."""

    model = models.Source
    list_display = [
        model.FieldNames.pk,
        'html',
        'date_string',
        model.FieldNames.location,
        'admin_source_link',
        'type',
    ]
    list_filter = [
        model.FieldNames.verified,
        HasContainerFilter,
        HasFileFilter,
        HasFilePageOffsetFilter,
        ImpreciseDateFilter,
        model.FieldNames.hidden,
        AttributeeFilter,
        TypeFilter,
    ]
    readonly_fields = SearchableModelAdmin.readonly_fields + [
        model.FieldNames.string,
        model.FieldNames.extra,
    ]
    search_fields = models.Source.searchable_fields
    ordering = ['date', model.FieldNames.string]
    inlines = [
        AttributeesInline,
        ContainersInline,
        ContainedSourcesInline,
        RelatedInline,
    ]
    autocomplete_fields = [model.FieldNames.file, model.FieldNames.location]

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
            models.Source.FieldNames.file,
            models.Source.FieldNames.location,
        )
        ordering = self.get_ordering(request)
        if ordering and ordering != models.Source.get_meta().ordering:
            qs = qs.order_by(*ordering)
        return qs

    def get_fields(self, request, model_instance=None):
        """Return reordered fields to be displayed in the admin."""
        fields = list(super().get_fields(request, model_instance))
        fields_to_move = (models.Source.FieldNames.string,)
        for field in fields_to_move:
            if field in fields:
                fields.remove(field)
                fields.insert(0, field)
        return fields

    def get_urls(self):
        """TODO: add docstring."""
        urls = super().get_urls()
        additional_urls = [
            path(
                'entity_search/',
                self.admin_site.admin_view(EntitySearchView.as_view(model_admin=self)),
                name='entity_search',
            ),
        ]
        return additional_urls + urls


class SpeechAdmin(SourceAdmin):
    """TODO: add docstring."""

    model = models.Speech
    list_display = ['string', model.FieldNames.location, 'date_string']
    search_fields = [model.FieldNames.string, 'location__name']


class SourcesInline(TabularInline):
    """TODO: add docstring."""

    model = models.Source
    extra = 0
    fields = [
        'verified',
        'hidden',
        'date_is_circa',
        'creators',
        model.FieldNames.url,
        'date',
        'publication_date',
    ]


admin_site.register(models.Source, SourceAdmin)
admin_site.register(models.Speech, SpeechAdmin)
admin_site.register(models.Interview, SpeechAdmin)
