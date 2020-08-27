from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.models.base import IrekuaModelBase
from irekua_database.models import CollectionType
from irekua_organisms.models import CollectionTypeOrganismType
from irekua_organisms.models import CollectionTypeOrganismCaptureType


class CollectionTypeOrganismConfig(IrekuaModelBase):
    collection_type = models.OneToOneField(
        CollectionType,
        on_delete=models.CASCADE,
        help_text=_('Collection Type to be configured.'),
        primary_key=True)

    use_organisms = models.BooleanField(
        db_column='use_organisms',
        verbose_name=_('use organisms'),
        help_text=_(
            'Boolean flag indicating whether organisms are to be used '
            'in this collection type.'),
        blank=False,
        null=False,
        default=False)

    organism_types = models.ManyToManyField(
        'OrganismType',
        through='CollectionTypeOrganismType',
        through_fields=('collection_type', 'organism_type'),
        verbose_name=_('organism types'),
        help_text=_(
            'Types of organisms that can be registered into '
            'collections of this type.'),
        blank=True)
    organism_capture_types = models.ManyToManyField(
        'OrganismCaptureType',
        verbose_name=_('organism capture types'),
        help_text=_(
            'Types of organism captures that can be registered into '
            'collections of this type.'),
        blank=True)

    class Meta:
        verbose_name = _('Collection Type Organism Configuration')
        verbose_name = _('Collection Type Organism Configurations')

        ordering = ['-created_on']

    def __str__(self):
        msg = _('%(col_type)s - Organism Configuration')
        params = dict(col_type=self.collection_type.name)
        return msg % params

    def validate_and_get_organism_type(self, organism_type):
        try:
            return CollectionTypeOrganismType.objects.get(organism_type=organism_type.id)
        except CollectionTypeOrganismType.DoesNotExist:
            msg = _(
                'Organism type %(organism_type)s is not accepted in collections of '
                'type %(col_type)s')
            params = dict(
                organism_type=organism_type.name,
                col_type=self.collection_type.name)
            raise ValidationError(msg % params)

    def validate_and_get_organism_capture_type(self, capture_type):
        try:
            return CollectionTypeOrganismCaptureType.objects.get(capture_type=capture_type.id)
        except CollectionTypeOrganismCaptureType.DoesNotExist:
            msg = _(
                'Organism capture type %(capture_type)s is not accepted in collections '
                'of type %(col_type)s')
            params = dict(
                capture_type=capture_type.name,
                col_type=self.collection_type.name)
            raise ValidationError(msg % params)
