from typing import Tuple

from django.db import models
from django.db.models import ManyToManyField, ForeignKey, CASCADE, SET_NULL
from taggit.models import TaggedItemBase

from history.fields import ArrayField
from history.fields import HTMLField
from history.models import Model, TaggableModel
from occurrences.models import Occurrence
from sources.models import Source, SourceReference, SourceFactDerivation


class TopicQuoteRelation(Model):
    topic = ForeignKey('Topic', related_name='topic_quote_relations', on_delete=CASCADE)
    quote = ForeignKey('quotes.Quote', related_name='quote_topic_relations', on_delete=CASCADE)


class OccurrenceTopicRelation(Model):
    topic = ForeignKey('topics.Topic', related_name='topic_occurrence_relations', on_delete=CASCADE)
    occurrence = ForeignKey('occurrences.Occurrence', related_name='occurrence_topic_relations', on_delete=CASCADE)
    weight = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1000)], default=500)


class EntityTopicRelation(Model):
    """Relation of a topic to an entity."""
    entity = ForeignKey('entities.Entity', related_name='entity_topic_relations', on_delete=CASCADE)
    topic = ForeignKey('topics.Topic', related_name='topic_entity_relations', on_delete=CASCADE)


class TopicRelation(Model):
    """A relationship between topics."""
    from_topic = ForeignKey('Topic', related_name='topics_related_to', on_delete=CASCADE)
    to_topic = ForeignKey('Topic', related_name='topics_related_from', on_delete=CASCADE)
    # relation_type = models.CharField(max_length=20, blank=True, null=True)


class Topic(TaggableModel):
    """A topic"""
    key = models.CharField(max_length=20, unique=True)
    parent = ForeignKey('self', related_name='children', null=True, blank=True, on_delete=SET_NULL)
    aliases = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    description = HTMLField(null=True, blank=True)
    related_occurrences = ManyToManyField('occurrences.Occurrence', related_name='related_topics',
                                          through=OccurrenceTopicRelation)
    related_entities = ManyToManyField('entities.Entity', related_name='related_topics',
                                       through='EntityTopicRelation', blank=True)
    related_quotes = ManyToManyField('quotes.Quote', related_name='related_topics',
                                     through=TopicQuoteRelation, blank=True)
    related_topics = ManyToManyField('self', related_name='topics_related',
                                     symmetrical=True, blank=True)

    searchable_fields = ['key', 'description', 'aliases']

    class Meta:
        ordering = ['key']

    def __str__(self):
        return self.key

    @property
    def related_topics_string(self) -> str:
        return ', '.join([str(topic) for topic in self.related_topics.all()])

    def natural_key(self) -> Tuple:
        return self.key,

    def add_relationship(self, topic, relation_type=None, symmetrical: bool = False):
        relationship, created = TopicRelation.objects.get_or_create(
            from_topic=self,
            to_topic=topic,
            relation_type=relation_type
        )
        if symmetrical:
            # avoid recursion by passing `symmetrical=False`
            topic.add_relationship(self, relation_type=relation_type, symmetrical=False)
        return relationship

    def remove_relationship(self, topic, symmetrical: bool = False):
        TopicRelation.objects.filter(
            from_topic=self,
            to_topic=topic
        ).delete()
        if symmetrical:
            # avoid recursion by passing `symmetrical=False`
            topic.remove_relationship(self, symmetrical=False)


class FactRelation(Model):
    class Meta:
        abstract = True


class EntityFactRelation(FactRelation):
    """Relation of a fact to an entity."""
    entity = ForeignKey('entities.Entity', related_name='entity_fact_relations', on_delete=CASCADE)
    fact = ForeignKey('Fact', related_name='fact_entity_relations', on_delete=CASCADE)


class TopicFactRelation(FactRelation):
    """A relation of a fact to a topic."""
    topic = ForeignKey(Topic, related_name='topic_fact_relations', on_delete=CASCADE)
    fact = ForeignKey('Fact', related_name='fact_topic_relations', on_delete=CASCADE)


class OccurrenceFactRelation(FactRelation):
    """A relation of a fact to an occurrence."""
    occurrence = ForeignKey('occurrences.Occurrence', related_name='occurrence_fact_relations', on_delete=CASCADE)
    fact = ForeignKey('Fact', related_name='fact_occurrence_relations', on_delete=CASCADE)


class FactSupport(FactRelation):
    supported_fact = ForeignKey('Fact', on_delete=CASCADE, related_name='supported_fact_supports')
    supportive_fact = ForeignKey('Fact', on_delete=CASCADE, related_name='supportive_fact_supports')


class Fact(Model):
    text = HTMLField()
    supportive_facts = ManyToManyField('self', related_name='supported_facts', through=FactSupport, symmetrical=False)
    sources = ManyToManyField(Source, related_name='derived_facts', through=SourceFactDerivation)
    related_entities = ManyToManyField('entities.Entity', related_name='facts', through=EntityFactRelation)
    related_topics = ManyToManyField(Topic, related_name='facts', through=TopicFactRelation)
    related_occurrences = ManyToManyField(Occurrence, related_name='facts', through=OccurrenceFactRelation)

    searchable_fields = ['text']

    def __str__(self):
        return self.text.text
