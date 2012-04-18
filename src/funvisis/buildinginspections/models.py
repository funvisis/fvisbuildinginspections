# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from funvisis.users.models import FVISUser
from photologue.models import Gallery
from funvisis.geo.buildings.models import Building


from fvislib.utils.djangorelated \
    import get_path_to_app_repo_ as get_path_to_app_repo

import os
import datetime
import time

class BuildingInspection(models.Model):

    # 1. General
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    init_time = models.DateTimeField(verbose_name=u'1.1 Hora inicio')
    end_time = models.DateTimeField(verbose_name=u'1.2 Hora culminación')
    code = models.CharField(
        verbose_name=u'1.3 Código', max_length=20, blank=True)

    # 2. Participants
    inspector = models.ForeignKey(
        FVISUser, related_name=u'building_inspector',
        verbose_name=u'2.1 Inspector')
    reviewer = models.ForeignKey(
        FVISUser,
        related_name=u'building_reviewer',
        verbose_name=u'2.2 Revisor',
        limit_choices_to={'user__groups__name': u'revisores'})
    supervisor = models.ForeignKey(
        FVISUser, related_name=u'building_supervisor',
        verbose_name=u'2.3 Supervisor',
                limit_choices_to={'user__groups__name': u'supervisores'})

    # 3. Interviewee
    interviewee_building_relationship = models.CharField(
        verbose_name=u'3.1 Relación con la Edif.', max_length=50)
    interviewee_name_last_name = models.CharField(
        verbose_name=u'3.2 Nombre y apellido', max_length=50)
    interviewee_phone_number = models.CharField(
        verbose_name=u'3.3 Teléfono', max_length=50, blank=True)
    interviewee_email = models.EmailField(
        verbose_name=u'3.4 Correo Electrónico', blank=True)

    # 4. Building
    building = models.ForeignKey(
        Building, related_name=u'building',
        verbose_name=u'Edificio')

    # 6. Carrying Capacity
    people = models.IntegerField(
        verbose_name=u'6.1 Número de personas que ocupan el inmueble')
    # occupation_during = models.CharField(
    #     max_length=10, verbose_name='6.2 Ocupación durante',
    #     choices=(
    #         (u'mañana', 'mañana'),
    #         ('tarde', 'tarde'),
    #         ('noche', 'noche'),),)
    occupation_during_morning = models.BooleanField(verbose_name=u'mañana')
    occupation_during_afternoon = models.BooleanField(verbose_name=u'tarde')
    occupation_during_evening = models.BooleanField(verbose_name=u'noche')

    # 13. Degree of degradation

    condition_of_concrete = models.CharField(
        verbose_name=u'13.1 Est. de Concreto',
        help_text='Agrietamiento en elementos estructurales' \
            ' y/o corrosión en acero de refuerzo',
        max_length=10,
        choices=(
            ('ninguno', 'Ninguno'),
            ('moderado', 'Moderado'),
            ('severo', 'Severo'),))
    condition_of_steel = models.CharField(
        verbose_name=u'13.2 Est. de Acero',
        help_text='Corrosión en elementos de acero y/o' \
            'deterioro de conexiones y/o pandeo',
        max_length=10,
        choices=(
            ('ninguno', 'Ninguno'),
            ('moderado', 'Moderado'),
            ('severo', 'Severo'),))
    fill_cracks_in_walls = models.CharField(
        verbose_name=u'13.3 Agrietamiento en paredes de relleno',
        max_length=10,
        choices=(
            ('ninguno', 'Ninguno'),
            ('moderado', 'Moderado'),
            ('severo', 'Severo'),))
    condition_of_upkeep = models.CharField(
        verbose_name=u'13.4 Estado general de mantenimiento ',
        max_length=10,
        choices=(
            ('bueno', 'Bueno'),
            ('regular', 'Regular'),
            ('bajo', 'Bajo'),))

    # 14. Observations
    observations = models.TextField(
        verbose_name=u'14. Observaciones', blank=True)

    # 15 Document Backup
    image_backup = models.FileField(
        verbose_name=u'15. Respaldo escaneado',
        upload_to=get_path_to_app_repo(
            project_name=settings.SETTINGS_MODULE.split('.')[0],
            app_name=__name__.split('.')[-2],
            model_name='Building'),
        null=True,
        blank=True)

    # 16 Gallery
    gallery = models.ForeignKey(
        Gallery, related_name=u'building_gallery',
        verbose_name=u'16 Galería de fotos')

    # __. Threat Index
    caracas = models.BooleanField(
        verbose_name=u'¿Es en Caracas?',
        help_text='Solo para el revisor o el supervisor',
        choices=(
            (True, 'Sí'),
            (False, 'No'),))
    national_level_zonification = models.IntegerField(
        verbose_name=u'Nivel nacional_zonificación',
        null=True, blank=True,
        help_text='Solo para el revisor o el supervisor',
        choices=((1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)))

    macrozone_ccs = models.CharField(
        max_length=20, blank=True,
        verbose_name=u'CCS_Macrozona',
        help_text='Solo para el revisor o el supervisor',
        choices=(
            ('sur', 'Sur'),
            ('centro_sur', 'Centro Sur'),
            ('centro_norte', 'Centro Norte'),
            ('norte', 'Norte')))
    microzone_ccs = models.CharField(
        max_length=3, blank=True,
        verbose_name=u'CCS_Microzona',
        help_text='Solo para el revisor o el supervisor',
        choices=(
            ('1-1', '1-1'),
            ('1-2', '1-2'),
            ('2-1', '2-1'),
            ('2-2', '2-2'),
            ('3-1', '3-1'),
            ('3-2', '3-2'),
            ('3-3', '3-3'),
            ('4-1', '4-1'),
            ('4-2', '4-2'),
            ('5', '5'),
            ('6', '6'),
            ('7-1', '7-1')))

    class Meta:
        verbose_name = u"Edificación"
        verbose_name_plural = u"Edificaciones"

    def __unicode__(self):
        return u"{0}:{1}:{2}".format(
            u' '.join(
                (
                    self.inspector.user.first_name,
                    self.inspector.user.last_name)).strip()
            or
            self.inspector, self.init_time, self.id)

    def has_topographic_effects(self):
        return \
            self.building_at == 'cima' \
            or \
            self.building_at == 'ladera' and self.ground_over

    def threat_index(self):
        '''[0.23, 1.0]'''
        from .analysis import \
            threat_index_by_macro_zones_caracas, \
            threat_index_by_macro_zones_national
        macro_zone_table = \
            threat_index_by_macro_zones_caracas \
            if self.caracas \
            else threat_index_by_macro_zones_national
        macro_zone_self_value = \
            self.macrozone_ccs \
            if self.caracas \
            else self.national_level_zonification

        try:
            return macro_zone_table[macro_zone_self_value][
                0 if not self.has_topographic_effects() else 1]
        except KeyError:
            return None

    def vulnerability_index(self):
        '''[6.5, 100.0]'''
        return 6.5

    def importance_index(self):
        '''[0.8, 1.0]'''
        return 0.8

    def priorization_index(self):
        return self.threat_index() * self.vulnerability_index() * \
            importance_index()

#VERIFICAR campos null y blank

