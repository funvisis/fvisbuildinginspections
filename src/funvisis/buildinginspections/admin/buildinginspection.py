# -*- coding: utf-8 -*-

from ..models import BuildingInspection

# from django.contrib import admin
from django.contrib.gis import admin
from funvisis.utils.decorators import conditional_fieldsets

@conditional_fieldsets
class BuildingInspectionAdmin(admin.GeoModelAdmin):

    fieldsets_base = (
        (
            u'1. Datos Generales',
            {
                'fields': (
                    'init_time',
                    'end_time',
                    'code')}),
        (
            u'2. Datos de los participantes',
            {
                'fields': (
                    # 'inspector',
                    'reviewer',
                    'supervisor')}),
        (
            u'3. Datos del entrevistado',
            {
                'fields': (
                    'interviewee_building_relationship',
                    'interviewee_name_last_name',
                    'interviewee_phone_number',
                    'interviewee_email')}),
        (
            u'Datos del edificio',
            {
                'fields': (
                    'building',)}),
        
        (
        #FIX NUMBERING
            u'6. Capacidad de ocupación',
            {
                'fields': (
                    'people',)}),
        (
            u'7. Períodos de ocupación',
            {
                'fields': (
                    'occupation_during_morning',
                    'occupation_during_afternoon',
                    'occupation_during_evening',)}),
        (
            u'14. Grado de deterioro',
            {
                'fields': (
                    'condition_of_concrete',
                    'condition_of_steel',
                    'fill_cracks_in_walls',
                    'condition_of_upkeep')}),
        (
            u'15. Observaciones',
            {
                'fields': (
                    'observations',)}),
        (
            u'16. Respaldo de la planilla',
            {
                'fields': (
                    'image_backup',)}),

        (   u'17. Imágenes de la estructura',
            {
                'fields': (
                    'gallery',)}),)

    fieldsets_super = (
        (
            u'Índice de amenaza',
            {
                'fields': (
                    'caracas',
                    'national_level_zonification',
                    'macrozone_ccs',
                    'microzone_ccs'),}),)

    conditioned_fieldsets = [
        (
            lambda request: True,
            fieldsets_base),

        (
            lambda request: \
                request.user.is_superuser or \
                request.user.groups.filter(name="supervisores") or \
                request.user.groups.filter(name="revisores"),
            fieldsets_super),
        ]



    date_hierarchy = 'init_time'

    def usage_list_display(self, obj):
        text_length = 50
        usage_fields = [
            'governmental',
            'firemen',
            'civil_defense',
            'police',
            'military',
            'popular_housing',
            'single_family',
            'multifamily',
            'medical_care',
            'educational',
            'sports_recreational',
            'cultural',
            'industrial',
            'commercial',
            'office',
            'religious',]
        result = ', '.join(
            [
                BuildingInspection._meta.get_field(_).verbose_name
                for _ in usage_fields
                if getattr(obj, _)] + [obj.other])

        return result

    list_display = (
        'inspector',
        'init_time',
#        'city',
#        'urbanization',
        'usage_list_display',
        )

    # list_filter = (
    #      'inspector',
    #     'city',)

    search_fields = [
        '^inspector__user__username',
        '^inspector__user__first_name',
        '^inspector__user__last_name',
#        '=city',
        'urbanization']


    # def get_form(self, request, obj=None, **kwargs):
    #     """
    #     Exclude some fields based on the request.user.
    #     """

    #     self.fieldsets = self.fieldsets_infra

    #     if (
    #         request.user.is_superuser or
    #         request.user.groups.filter(name="supervisores") or
    #         request.user.groups.filter(name="revisores")):

    #         self.fieldsets += self.fieldsets_super # FIXME: use some
    #                                                # argument or
    #                                                # custom ModelAdmin
    #                                                # field to mark the
    #                                                # fields to
    #                                                # remove. Later,
    #                                                # make a custom
    #                                                # ModelAdmin
    #                                                # classdefine that
    #                                                # field, and others
    #                                                # like the
    #                                                # condition to
    #                                                # evaluate to
    #                                                # remove the
    #                                                # fields.

    #     if obj is not None and not(
    #                 request.user.is_superuser or
    #                 request.user.groups.filter(name="supervisores") or
    #                 request.user.groups.filter(name="revisores")):
    #         self.readonly_fields = ('supervisor', 'reviewer')
    #     else:
    #         try:
    #             del self.readonly_fields
    #         except AttributeError:
    #             pass

    #     return super(BuildingAdmin, self).get_form(request, obj=obj, **kwargs)

    def save_model(self, request, obj, form, change): # The logged
                                                      # user is going
                                                      # to be the
                                                      # inspector
        if not change: # Only adding sets the inspector
            obj.inspector = request.user.fvisuser
        obj.save()

    def queryset(self, request):

        if request.user.groups.filter(name='supervisores') or \
                request.user.is_superuser:
            return BuildingInspection.objects.all()

        return BuildingInspection.objects.filter(inspector=request.user.fvisuser)


    class Media:
        js = ('js/admin/custom.js', )
