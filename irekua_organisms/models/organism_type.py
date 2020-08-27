from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from irekua_database.models.base import IrekuaModelBase
from irekua_database.models import TermType
from irekua_database.utils import validate_JSON_schema
from irekua_database.utils import validate_JSON_instance
from irekua_database.utils import simple_JSON_schema


class OrganismType(IrekuaModelBase):
    name = models.CharField(
        max_length=64,
        db_column='name',
        verbose_name=_('name'),
        unique=True,
        help_text=_('Name of organism type'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of organism type'),
        blank=False)

    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Organism type icon'),
        upload_to='images/organism_types/',
        blank=True,
        null=True)

    term_types = models.ManyToManyField(
        TermType,
        verbose_name=_('term types'),
        help_text=_('Valid term types to describe the organism'),
        blank=True)
    identification_info_schema = models.JSONField(
        db_column='identification_info_schema',
        verbose_name=_('identification information schema'),
        help_text=_('JSON Schema for identification information.'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])

    is_multi_organism = models.BooleanField(
        db_column='is_multi_organism',
        verbose_name=_('is multi organism'),
        help_text=_(
            'Boolean flag that indicates whether this organism'
            'may be composed by multiple organisms.'),
        blank=False,
        null=False,
        default=False)

    class Meta:
        verbose_name =_('Organism Type')
        verbose_name_plural =_('Organism Types')
        ordering = ['-created_on']

    def __str__(self):
        return str(self.name)

    def validate_id_info(self, id_info):
        try:
            validate_JSON_instance(
                schema=self.additional_id_info_schema,
                instance=id_info)
        except ValidationError as error:
            msg = _(
                'Invalid identification information for organism '
                'type %(type)s. Error: %(error)s')
            params = dict(type=self.name, error=', '.join(error.messages))
            raise ValidationError(msg, params=params)

    def validate_term(self, term):
        if not self.term_types.filter(id=term.term_type.id).exists():
            msg = _(
                'Terms of type %(term_type)s are not allowed for organism '
                ' of type %(capture_type)s. Term: %(term)s')
            params = dict(
                term_type=term.term_type.name,
                capture_type=self.name,
                term=term.value)
            raise ValidationError(msg % params)
