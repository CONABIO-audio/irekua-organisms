from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from irekua_database.utils import empty_JSON
from irekua_database.models.base import IrekuaModelBaseUser
from irekua_database.models import Collection
from irekua_database.models import Term
from irekua_database.models import Item


class Organism(IrekuaModelBaseUser):
    collection = models.ForeignKey(
        Collection,
        db_column='collection_id',
        verbose_name=_('collection'),
        help_text=_('Collection to which this organism belongs'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)
    organism_type = models.ForeignKey(
        'OrganismType',
        db_column='organism_type_id',
        verbose_name=_('organism type'),
        help_text=_('Type of organism'),
        on_delete=models.PROTECT,
        blank=False,
        null=False)

    name = models.CharField(
        max_length=64,
        db_column='name',
        verbose_name=_('name'),
        unique=True,
        help_text=_('A textual name or label assigned to an Organism instance'),
        blank=True,
        null=True)
    remarks = models.TextField(
        db_column='remarks',
        verbose_name=_('remarks'),
        help_text=_('Comments or notes about the Organism instance'),
        blank=True)

    identification_info = models.JSONField(
        db_column='identification_info',
        default=empty_JSON,
        verbose_name=_('identification info'),
        help_text=_('Organism identification information.'),
        blank=True,
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
        help_text=_('Description of the organism'),
        blank=True)

    items = models.ManyToManyField(
        Item,
        verbose_name=_('items'),
        help_text=_('Items associated to this organism'))

    class Meta:
        verbose_name = _('Organism')
        verbose_name_plural = _('Organisms')
        ordering = ['-created_on']

    def __str__(self):
        if self.name:
            return str(self.name)

        msg = _('Organism %(id)s')
        params = dict(id=self.id)
        return msg % params

    def clean(self):
        super().clean()

        collection = sampling_event.collection
        collection_type = collection.collection_type

        try:
            organism_config = collection_type.collectiontypeorganismconfig
        except ObjectDoesNotExist:
            raise ValidationError(_('This collection does not allow organisms'))

        if not organism_config.use_organisms:
            raise ValidationError(_('This collection does not allow organisms'))

        try:
            self.organism_type.validate_id_info(self.identification_info)
        except ValidationError as error:
            raise ValueError({'identification_info': error})

        try:
            organism_type = organism_config.validate_and_get_organism_type(self.organism_type)
        except ValidationError as error:
            raise ValidationError({'organism_type': error})

        try:
            organism_type.validate_additional_metadata(self.additional_metadata)
        except ValidationError as error:
            raise ValidationError({'additional_metadata': error})
