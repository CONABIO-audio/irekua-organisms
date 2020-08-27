from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from irekua_database.models.base import IrekuaModelBase

from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema


class CollectionTypeOrganismCaptureType(IrekuaModelBase):
    collection_type_organism_config = models.ForeignKey(
        'CollectionTypeOrganismConfig',
        on_delete=models.CASCADE,
        db_column='collection_type_organism_config_id',
        verbose_name=_('collection type organism config'),
        help_text=_('Collection type organism configuration'),
        blank=False,
        null=False)
    organism_capture_type = models.ForeignKey(
        'OrganismCaptureType',
        on_delete=models.PROTECT,
        db_column='organism_capture_type_id',
        verbose_name=_('organism capture type'),
        help_text=_('Organism capture type to be registered to the collection type'),
        blank=False,
        null=False)
    metadata_schema = models.JSONField(
        db_column='metadata_schema',
        verbose_name=_('additional metadata schema'),
        help_text=_(
            'JSON Schema for additional metadata of this type of '
            'organism capture in this type of collections.'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])

    class Meta:
        verbose_name = _('Collection Type Organism Capture Type')
        verbose_name = _('Collection Type Organism Capture Types')

        ordering = ['-created_on']
        unique_together = (
            ('collection_type_organism_config', 'organism_capture_type'),
        )

    def validate_additional_metadata(self, metadata):
        try:
            validate_JSON_instance(
                schema=self.metadata_schema,
                instance=metadata)
        except ValidationError as error:
            msg = _(
                'Invalid additional metadata for organism capture '
                'type %(type)s. Error: %(error)s')
            params = dict(type=self.name, error=', '.join(error.messages))
            raise ValidationError(msg, params=params)

    def clean(self):
        super().clean()

        organism_type = self.organism_capture_type.organism_type
        organism_config = self.collection_type_organism_config

        try:
            organism_config.validate_and_get_organism_type(organism_type)
        except ValidationError as error:
            raise ValidationError({'organism_capture_type': error})

        collection_type = organism_config.collection_type
        device_type = self.organism_capture_type.device_type
        try:
            collection_type.validate_and_get_device_type(device_type)
        except ValidationError as error:
            raise ValidationError({'organism_capture_type': error})
