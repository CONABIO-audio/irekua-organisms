from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.models.base import IrekuaModelBase
from irekua_database.models import DeviceType
from irekua_database.models import TermType


class OrganismCaptureType(IrekuaModelBase):
    name = models.CharField(
        max_length=64,
        db_column='name',
        verbose_name=_('name'),
        unique=True,
        help_text=_('Name of organism capture type'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of organism capture type'),
        blank=False)

    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Organism capture type icon'),
        upload_to='images/organism_types/',
        blank=True,
        null=True)

    organism_type = models.ForeignKey(
        'OrganismType',
        on_delete=models.CASCADE,
        db_column='organism_type_id',
        verbose_name=_('organism type'),
        help_text=_('Organism type being captured'),
        blank=False,
        null=False)
    device_type = models.ForeignKey(
        DeviceType,
        on_delete=models.PROTECT,
        db_column='device_type_id',
        verbose_name=_('device type'),
        help_text=_('Device type used for capture'),
        blank=False,
        null=False)

    term_types = models.ManyToManyField(
        TermType,
        verbose_name=_('term types'),
        help_text=_('Valid term types to describe the organism capture'),
        blank=True)

    class Meta:
        verbose_name = _('Organism Capture Type')
        verbose_name_plural = _('Organism Capture Types')
        ordering = ['-created_on']

    def __str__(self):
        return str(self.name)

    def validate_term(self, term):
        if not self.term_types.filter(id=term.term_type.id).exists():
            msg = _(
                'Terms of type %(term_type)s are not allowed for organism captures '
                ' of type %(capture_type)s. Term: %(term)s')
            params = dict(
                term_type=term.term_type.name,
                capture_type=self.name,
                term=term.value)
            raise ValidationError(msg % params)
