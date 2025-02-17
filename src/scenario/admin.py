from django.contrib import admin
from django import forms
from .models import Project, Scenario, Structures, ArealFeatureLookup, \
    CostItem, StructureCostItemDefaultFactors, CostItemDefaultCosts, CostItemDefaultEquations, \
    ScenarioStructure, ScenarioCostItemUserCosts, StructureCostItemUserFactors, ScenarioArealFeature


class ObjectAdmin(admin.ModelAdmin):
    ordering = ['-order']


def custom_titled_filter(title):
    """
    this allows overriding the name shown in the right-side FILTER panel

    :param title:
    :return:
    """
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


@admin.display(description="Affiliation", ordering='project__user__organization_tx')
def user_affiliation(obj):
    return "%s" % obj.project.user.organization_tx


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user_fullname', 'user_affiliation', 'user_type', 'project_title', 'create_date', 'modified_date')
    list_display_links = ('project_title',)
    list_filter = (('user__profile__user_type', custom_titled_filter("User Type")),)

    readonly_fields = ['create_date', 'modified_date']

    @admin.display(description='User Name', ordering='user__name')
    def user_fullname(self, obj):
        return "%s" % obj.user.get_full_name()

    @admin.display(description='Affiliation', ordering='user__organization_tx')
    def user_affiliation(self, obj):
        return "%s" % obj.user.organization_tx

    @admin.display(ordering='user__profile__user_type')
    def user_type(self, obj):
        return "%s" % obj.user.profile.user_type

    @admin.display(description='Project', ordering='project_title')
    def project_title(self, obj):
        return "%s" % obj.project_title

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(Project, ProjectAdmin)


class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('user_fullname', user_affiliation, 'user_type',
                    'project_title', 'scenario_title', 'create_date', 'modified_date')
    list_display_links = ('scenario_title',)
    list_filter = (('project__user__profile__user_type', custom_titled_filter("User Type")),
                   ('project__user__name', custom_titled_filter("User Name")),)
    exclude = ('areal_features', 'conventional_structures', 'nonconventional_structures', 'counter', 'scenario_date')

    readonly_fields = ['create_date', 'modified_date']

    @admin.display(description='User Name', ordering='project__user__name')
    def user_fullname(self, obj):
        return "%s" % obj.project.user.get_full_name()

    @admin.display(ordering='project__user__profile__user_type')
    def user_type(self, obj):
        return "%s" % obj.project.user.profile.user_type

    @admin.display(description='Project', ordering='project__project_title')
    def project_title(self, obj):
        return "%s" % obj.project.project_title

    @admin.display(ordering='scenario_title')
    def scenario_title(self, obj):
        return "%s" % obj.scenario_title

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(Scenario, ScenarioAdmin)


class ArealFeatureLookupAdmin(admin.ModelAdmin):
    list_display = ('sort_nu', 'code', 'name')
    list_display_links = ('name',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(ArealFeatureLookupAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'help_text':
            field.widget = forms.Textarea(attrs={'cols': 80, 'rows': 4})
        return field

    # you can delete the ArealFeatureLookup - but it will delete all the associated data
    def has_delete_permission(self, request, obj=None):
        return True

class StructuresAdmin(admin.ModelAdmin):
    list_display = ('sort_nu', 'classification', 'code', 'name', 'units', 'help_text',)
    list_display_links = ('name',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(StructuresAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'help_text':
            field.widget = forms.Textarea(attrs={'cols': 80, 'rows': 4})
        return field

    # I enabled deleting Structures to support ad-hoc changing of what is available
    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions

    def has_delete_permission(self, request, obj=None):
        return True


class CostItemAdmin(StructuresAdmin):
    list_display = ('sort_nu', 'code', 'name', 'units', 'help_text')
    list_display_links = ('name',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(CostItemAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'help_text':
            field.widget = forms.Textarea(attrs={'cols': 80, 'rows': 4})
        return field


@admin.display(description='Sort #', ordering='costitem__sort_nu')
def costitem_sort_nu(obj):
    return obj.costitem.sort_nu


@admin.display(description='Cost Item', empty_value='unknown', ordering='costitem__name')
def costitem_name(obj):
    return "%s" % obj.costitem.name


class CostItemDefaultCostsAdmin(StructuresAdmin):
    list_display = (costitem_sort_nu, 'costitem_name', 'costitem_units', 'cost_type2',
                    'valid_start_date_tx', 'value_numeric',  # 'db_75pct_va',
                    'created_date', 'modified_date'
                    # 'replacement_life', 'o_and_m_pct',
                    # 'equation'
                    )
    list_display_links = ('costitem_name',)
    readonly_fields = ['created_date', 'modified_date']
    search_fields = ('costitem__name', 'cost_type',
                    'valid_start_date_tx')

    exclude = ('rsmeans_va','db_25pct_va','db_50pct_va','db_75pct_va')

    @admin.display(description='Bid Units', empty_value='unknown', ordering='costitem__units')
    def costitem_units(self, obj):
        return "%s" % obj.costitem.units

    @admin.display(description='Cost Type')
    def cost_type2(self, obj):
        return "%s" % obj.cost_type

    @admin.display(description='Cost Item', empty_value='unknown', ordering='costitem__name')
    def costitem_name(self, obj):
        return "%s" % obj.costitem.name

    model = CostItemDefaultCosts
    def get_queryset(self, request):
        return super(CostItemDefaultCostsAdmin, self)\
            .get_queryset(request).select_related(
            'costitem')

class CostItemDefaultEquationsAdmin(StructuresAdmin):
    list_display = (costitem_sort_nu, costitem_name, 'equation_tx',
                    'replacement_life', 'o_and_m_pct',
                    # 'a_area', 'z_depth', 'd_density', 'n_number'
                    )
    list_display_links = (costitem_name,)

    model = CostItemDefaultEquations
    def get_queryset(self, request):
        return super(CostItemDefaultEquationsAdmin, self)\
            .get_queryset(request).select_related(
            'costitem')


class StructureCostItemDefaultFactorsAdmin(StructuresAdmin):
    """
    this is tied to both Structure (parent) and Cost Item (child)
    """
    list_display = ('structure_name', 'costitem_name', 'costitem_units','a_area', 'z_depth', 'd_density', 'n_number')
    list_display_links = ('structure_name', 'costitem_name',)
    list_filter = (('structure__name', custom_titled_filter("Structure Name")),
                   ('costitem__name', custom_titled_filter('Cost Item Name')))

    @admin.display(empty_value='unknown', ordering='structure__name')
    def structure_name(self, obj):
        return "%s" % obj.structure.name

    @admin.display(empty_value='unknown', ordering='costitem__name')
    def costitem_name(self, obj):
        return "%s" % obj.costitem.name

    @admin.display(empty_value='unknown')
    def costitem_units(self, obj):
        return "%s" % obj.costitem.units

    @admin.display(description='Area (a)')
    def a_area(self, obj):
        return "%s" % obj.a_area

    @admin.display(description='Depth (z)')
    def z_depth(self, obj):
        return obj.z_depth

    @admin.display(description='Density (d)')
    def d_density(self, obj):
        return obj.d_density

    @admin.display(description='Count (n)')
    def n_number(self, obj):
        return obj.z_depth

    model = StructureCostItemDefaultFactors
    def get_queryset(self, request):
        return super(StructureCostItemDefaultFactorsAdmin, self)\
            .get_queryset(request)\
            .select_related(
                'structure',
                'costitem',
            )  \
            .only('structure__name', 'structure__sort_nu',
                  'costitem__name', 'costitem__units', 'costitem__sort_nu',
                  'a_area', 'z_depth', 'd_density', 'n_number',
                  )\
            .order_by('structure__sort_nu', 'costitem__sort_nu',)



@admin.display(description='User', ordering='scenario__project__user__name')
def user_name(obj):
    return "%s" % obj.scenario.project.user.name


@admin.display(description='Type', ordering='scenario__project__user__profile__user_type')
def user_type(obj):
    return "%s" % obj.scenario.project.user.profile.user_type


@admin.display(description='Project', ordering='scenario__project__project_title')
def scenario_project_title(obj):
    return "%s" % obj.scenario.project.project_title


@admin.display(description='Scenario', ordering='scenario__scenario_title')
def scenario_title(obj):
    return "%s" % obj.scenario.scenario_title


@admin.display(description='Cost Source', ordering='cost_source')
def cost_source(obj):
    source = obj.cost_source
    if source == 'user':
        source = 'User'
    elif obj.default_cost is not None:
        source = str(obj.default_cost.cost_type)
    return "%s" % source


@admin.display(description='Year (revision)')
def valid_start_date_tx(obj):
    source = obj.cost_source
    if source == 'user':
        source = obj.base_year
    elif obj.default_cost is not None:
        source = obj.default_cost.valid_start_date_tx
    return "%s" % source


@admin.display(description='Unit Cost', ordering='user_input_cost')
def user_input_cost(obj):
    source = obj.cost_source
    input_cost = None
    if source == 'user':
        input_cost = obj.user_input_cost
    elif obj.default_cost is not None:
        input_cost = obj.default_cost.value_numeric

    # input_cost = obj.user_input_cost
    # if not input_cost:
    #     input_cost = 'N/A'
    return "%s" % input_cost


@admin.display(description='Rep Life (yrs)', ordering='replacement_life')
def replacement_life(obj):
    return "%s" % obj.replacement_life


@admin.display(description='Annual O&M (%)', ordering='o_and_m_pct')
def o_and_m_pct(obj):
    return "%s" % obj.o_and_m_pct

@admin.display(description='areal_feature_name')
def areal_feature_name(obj):
    return "%s" % obj.areal_feature.name

@admin.display(description='structure_name')
def structure_name(obj):
    return "%s" % obj.structure.name

@admin.display(description='First Year Maintenance', ordering='first_year_maintenance')
def first_year_maintenance(obj):
    return "%s" % obj.first_year_maintenance

class ScenarioArealFeatureAdmin(admin.ModelAdmin):
    list_display = (user_name, user_type, scenario_project_title, scenario_title, areal_feature_name,
                    'area2', 'is_checked')
    list_display_links = (areal_feature_name,)
    list_filter = (
        ('scenario__project__user__profile__user_type', custom_titled_filter("User Type")),
        ('scenario__project__user__name', custom_titled_filter("User Name")),
        ('areal_feature__name', custom_titled_filter('areal_feature Name'))
    )
    search_fields = ('scenario__scenario_title', 'areal_feature_name',
                     )
    ordering = ['scenario__scenario_title', ]

    @admin.display(description='Area (sf)', ordering='area')
    def area2(self, obj):
        if obj.area is None:
            return '--'
        return "{: <10,}".format(obj.area)

    @admin.display(description='Checked ')
    def is_checked(self, obj):
        return obj.is_checked

    model = ScenarioArealFeature
    def get_queryset(self, request):
        return super(ScenarioArealFeatureAdmin, self)\
            .get_queryset(request)\
            .select_related(
                'scenario', 'scenario__project', 'scenario__project__user',
                'scenario__project__user__profile',
                'areal_feature',
            )

class ScenarioStructureAdmin(admin.ModelAdmin):
            list_display = (user_name, user_type, scenario_project_title,
                            scenario_title, structure_name,
                            'area2', 'is_checked')
            list_display_links = (structure_name,)
            list_filter = (
                ('scenario__project__user__profile__user_type', custom_titled_filter("User Type")),
                ('scenario__project__user__name', custom_titled_filter("User Name")),
                ('structure__name', custom_titled_filter('Structure Name'))
            )
            search_fields = ('scenario__scenario_title', 'structure_name',
                             )
            ordering = ['scenario__scenario_title', 'structure__sort_nu',]

            @admin.display(description='Area (sf)')
            def area2(self, obj):
                if obj.area is None:
                    return '--'
                return "{: <10,}".format(obj.area)

            @admin.display(description='Checked ')
            def is_checked(self, obj):
                return obj.is_checked

            model = ScenarioStructure

            def get_queryset(self, request):
                return super(ScenarioStructureAdmin, self) \
                    .get_queryset(request) \
                    .select_related(
                    'scenario', 'scenario__project', 'scenario__project__user',
                    'scenario__project__user__profile',
                    'structure',
                )


class ScenarioCostItemUserCostsAdmin(admin.ModelAdmin):
    list_display = (user_name, user_type, scenario_project_title, scenario_title, costitem_name,
                    cost_source, valid_start_date_tx, user_input_cost,
                    replacement_life, o_and_m_pct, 'modified_date')
    list_display_links = (costitem_name,)
    list_filter = (
        ('scenario__project__user__profile__user_type', custom_titled_filter("User Type")),
        ('scenario__project__user__name', custom_titled_filter("User Name")),
        ('costitem__name', custom_titled_filter('Cost Item Name'))
    )
    search_fields = ('scenario__scenario_title', 'costitem__name',
                    )
    ordering = ['scenario__scenario_title', 'costitem__sort_by',]

    exclude = ('first_year_maintenance',)

    model = ScenarioCostItemUserCosts
    def get_queryset(self, request):
        return super(ScenarioCostItemUserCostsAdmin, self)\
            .get_queryset(request)\
            .select_related(
                'scenario', 'scenario__project', 'scenario__project__user',
                'scenario__project__user__profile',
                'costitem', 'default_cost'
            ) \
            .only('scenario__scenario_title', 'scenario__project__project_title',
                  'scenario__project__user__name', 'scenario__project__user__profile__user_type',
                  'user_input_cost', 'user_input_cost_currency',
                  'replacement_life', 'o_and_m_pct', 'cost_source', 'modified_date', 'base_year',
                  'costitem__name',
                  'default_cost__cost_type',  'default_cost__value_numeric', 'default_cost__value_numeric_currency',
                  'default_cost__valid_start_date_tx',
                  )

    def get_actions(self, request):
        actions = super().get_actions(request)
        # if 'delete_selected' in actions:
        #     del actions['delete_selected']
        return actions

    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False


@admin.display(description='Structure Name', empty_value='unknown', ordering='structure__name')
def structure_name(obj):
    return "%s" % obj.structure.name


class StructureCostItemUserFactorsAdmin(admin.ModelAdmin):
    list_display = (user_name, user_type, scenario_project_title, scenario_title,
                    structure_name, costitem_name,
                    # cost_source, user_input_cost, 'base_year',
                    # replacement_life, o_and_m_pct, first_year_maintenance
                    )
    list_display_links = (costitem_name,)
    list_filter = (('scenario__project__project_title', custom_titled_filter("Project")),
                   ('costitem__name', custom_titled_filter('Cost Item Name')))
    def get_actions(self, request):
        actions = super().get_actions(request)
        # if 'delete_selected' in actions:
        #     del actions['delete_selected']
        return actions

    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False
    model = StructureCostItemUserFactors
    def get_queryset(self, request):
        return super(StructureCostItemUserFactorsAdmin, self)\
            .get_queryset(request)\
            .select_related(
                'scenario', 'scenario__project', 'scenario__project__user',
                'scenario__project__user__profile',
                'structure',
                'costitem',
            ) \
            .only('scenario__scenario_title', 'scenario__project__project_title',
                  'scenario__project__user__name', 'scenario__project__user__profile__user_type',
                  'structure__name',
                  'costitem__name',
                  'checked', 'a_area', 'z_depth', 'd_density', 'n_number',
                  )


admin.site.register(ArealFeatureLookup, ArealFeatureLookupAdmin)
admin.site.register(Structures, StructuresAdmin)
admin.site.register(CostItem, CostItemAdmin)
admin.site.register(CostItemDefaultCosts, CostItemDefaultCostsAdmin)
admin.site.register(CostItemDefaultEquations, CostItemDefaultEquationsAdmin)
admin.site.register(StructureCostItemDefaultFactors, StructureCostItemDefaultFactorsAdmin)
admin.site.register(ScenarioArealFeature, ScenarioArealFeatureAdmin)
admin.site.register(ScenarioStructure, ScenarioStructureAdmin)
admin.site.register(ScenarioCostItemUserCosts, ScenarioCostItemUserCostsAdmin)
admin.site.register(StructureCostItemUserFactors, StructureCostItemUserFactorsAdmin)
