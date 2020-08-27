from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from irekua_database.utils import empty_JSON
from irekua_database.models.base import IrekuaModelBaseUser
from irekua_database.models import SamplingEventDevice
from irekua_database.models import Item
from irekua_database.models import Term


class OrganismCapture(IrekuaModelBaseUser):
    organism_capture_type = models.ForeignKey(
        'OrganismCaptureType',
        db_column='organism_capture_type_id',
        verbose_name=_('organism capture type'),
        help_text=_('Capture type'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)

    sampling_event_device = models.ForeignKey(
        SamplingEventDevice,
        db_column='sampling_event_device_id',
        verbose_name=_('sampling event device'),
        help_text=_('Device used to capture this organism'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)
    organism = models.ForeignKey(
        'Organism',
        db_column='organism_id',
        verbose_name=_('organism'),
        help_text=_('Captured organism'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)

    additional_metadata = models.JSONField(
        db_column='additional_metadata',
        default=empty_JSON,
        verbose_name=_('additional metadata'),
        help_text=_('Additional organism metadata'),
        blank=True,
        null=False)

    labels = models.ManyToManyField(
        Term,
        verbose_name=_('labels'),
        help_text=_('Description of the organism capture'),
        blank=True)
    items = models.ManyToManyField(
        Item,
        verbose_name=_('items'),
        help_text=_('Items associated to this organism'))

    class Meta:
        verbose_name =_('Organism Capture')
        verbose_name_plural =_('Organism Captures')
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.organism_capture_type.name} {self.id}'

    def clean(self):
        super().clean()

        sampling_event = sampling_event_device.sampling_event
        collection = sampling_event.collection
        collection_type = collection.collection_type

        try:
            organism_config = collection_type.collectiontypeorganismconfig
        except ObjectDoesNotExist:
            raise ValidationError(_('This collection does not allow organisms'))

        if not organism_config.use_organisms:
            raise ValidationError(_('This collection does not allow organisms'))

        try:
            capture_type = organism_config.validate_and_get_organism_capture_type(self.organism_capture_type)
        except ValidationError as error:
            raise ValidationError({'organism_capture_type': error})

        try:
            capture_type.validate_additional_metadata(self.additional_metadata)
        except ValidationError as error:
            raise ValidationError({'additional_metadata': error})
