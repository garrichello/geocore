# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccumulationMode(models.Model):
    name = models.CharField(unique=True, max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accumulation_mode'

    def __str__(self):
        return self.name


class ArgumentType(models.Model):
    label = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'argument_type'

    def __str__(self):
        return self.label


class ArgumentsGroup(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=145, blank=True, null=True)
    argument_type = models.ForeignKey('ArgumentType', models.CASCADE)
    processor = models.ManyToManyField('Processor', through='ArgumentsGroupHasProcessor')
    specific_parameter = models.ManyToManyField('SpecificParameter', through='ArgumentsGroupHasSpecificParameter')

    class Meta:
        managed = False
        db_table = 'arguments_group'

    def __str__(self):
        return self.name


class ArgumentsGroupHasProcessor(models.Model):
    arguments_group = models.ForeignKey('ArgumentsGroup', models.CASCADE)
    processor = models.ForeignKey('Processor', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'arguments_group_has_processor'
        unique_together = (('arguments_group', 'processor'),)


class ArgumentsGroupHasSpecificParameter(models.Model):
    arguments_group = models.ForeignKey('ArgumentsGroup', models.CASCADE)
    specific_parameter = models.ForeignKey('SpecificParameter', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'arguments_group_has_specific_parameter'
        unique_together = (('arguments_group', 'specific_parameter'),)


class Collection(models.Model):
    label = models.CharField(unique=True, max_length=45)
    url = models.CharField(max_length=255, blank=True, null=True)
    organization = models.ForeignKey('Organization', models.CASCADE)
    language = models.ManyToManyField('Language', through='CollectionI18N')

    class Meta:
        managed = False
        db_table = 'collection'

    def __str__(self):
        return self.label


class CollectionI18N(models.Model):
    collection = models.ForeignKey('Collection', models.CASCADE)
    language = models.ForeignKey('Language', models.CASCADE)
    name = models.CharField(max_length=155, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'collection_i18n'
        unique_together = (('collection', 'language'), ('name', 'language'),)

    def __str__(self):
        return self.name


class ComputingModule(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'computing_module'

    def __str__(self):
        return self.name


class ComputingSystem(models.Model):
    name = models.CharField(unique=True, max_length=80)
    type = models.ForeignKey('ComputingSystemType', models.DO_NOTHING)
    ip = models.CharField(max_length=256)
    cmd = models.CharField(max_length=256)
    user = models.CharField(max_length=64, blank=True, null=True)
    passwd = models.CharField(max_length=256, blank=True, null=True)
    temp_dir = models.CharField(max_length=256, blank=True, null=True)
    is_default = models.IntegerField()
    external_temp_dir = models.CharField(max_length=256)
    comment = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'computing_system'

    def __str__(self):
        return self.name


class ComputingSystemType(models.Model):
    name = models.CharField(max_length=60)
    cmd_type = models.CharField(max_length=60)
    comment = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'computing_system_type'

    def __str__(self):
        return self.name


class Conveyor(models.Model):

    class Meta:
        managed = False
        db_table = 'conveyor'


class Data(models.Model):
    dataset = models.ForeignKey('Dataset', models.CASCADE)
    specific_parameter = models.ForeignKey('SpecificParameter', models.CASCADE)
    property = models.ForeignKey('Property', models.CASCADE)
    property_value = models.ForeignKey('PropertyValue', models.CASCADE)
    units = models.ForeignKey('Units', models.CASCADE)
    variable = models.ForeignKey('Variable', models.CASCADE, related_name='variable')
    file = models.ForeignKey('File', models.CASCADE)
    levels_variable = models.ForeignKey('Variable', models.CASCADE, blank=True, null=True, related_name='levels_variable')
    root_dir = models.ForeignKey('RootDir', models.CASCADE)
    scale = models.FloatField()
    offset = models.FloatField()

    class Meta:
        managed = False
        db_table = 'data'


class DataKind(models.Model):
    name = models.CharField(unique=True, max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_kind'

    def __str__(self):
        return self.name


class DataVariable(models.Model):
    label = models.CharField(max_length=45, blank=True, null=True)
    description = models.CharField(max_length=45, blank=True, null=True)
    units = models.ForeignKey('Units', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'data_variable'

    def __str__(self):
        return self.label


class Dataset(models.Model):
    collection = models.ForeignKey('Collection', models.CASCADE)
    resolution = models.ForeignKey('Resolution', models.CASCADE)
    scenario = models.ForeignKey('Scenario', models.CASCADE)
    data_kind = models.ForeignKey('DataKind', models.CASCADE)
    description = models.CharField(unique=True, max_length=45, blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    time_start = models.CharField(max_length=10)
    time_end = models.CharField(max_length=10)
    file_type = models.ForeignKey('FileType', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'dataset'

    def __str__(self):
        return self.description if self.description is not None else ''


class Edge(models.Model):
    conveyor = models.ForeignKey('Conveyor', models.CASCADE)
    from_vertex = models.ForeignKey('Vertex', models.CASCADE, related_name='from_vertex')
    from_output = models.IntegerField()
    to_vertex = models.ForeignKey('Vertex', models.CASCADE, related_name='to_vertex')
    to_input = models.IntegerField()
    data_variable = models.ForeignKey(DataVariable, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'edge'
        unique_together = (('conveyor', 'from_vertex', 'from_output', 'to_vertex', 'to_input'),)


class File(models.Model):
    name_pattern = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'file'

    def __str__(self):
        return self.name_pattern


class FileType(models.Model):
    name = models.CharField(unique=True, max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'file_type'

    def __str__(self):
        return self.name


class Geoportal(models.Model):
    name = models.CharField(max_length=64)
    comment = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geoportal'

    def __str__(self):
        return self.name


class GuiElement(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    language = models.ManyToManyField('Language', through='GuiElementI18N')

    class Meta:
        managed = False
        db_table = 'gui_element'

    def __str__(self):
        return self.name


class GuiElementI18N(models.Model):
    gui_element = models.ForeignKey('GuiElement', models.CASCADE)
    language = models.ForeignKey('Language', models.CASCADE)
    caption = models.CharField(unique=True, max_length=145, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gui_element_i18n'
        unique_together = (('gui_element', 'language'),)

    def __str__(self):
        return self.caption


class Language(models.Model):
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'language'
    
    def __str__(self):
        return self.name


class Level(models.Model):
    label = models.CharField(unique=True, max_length=45)
    levels_group = models.ManyToManyField("LevelsGroup", through='LevelsGroupHasLevel', related_name='levels_group')

    class Meta:
        managed = False
        db_table = 'level'


class LevelI18N(models.Model):
    level = models.ForeignKey('Level', models.CASCADE)
    language = models.ForeignKey('Language', models.CASCADE)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'level_i18n'
        unique_together = (('level', 'language'), ('language', 'name'),)

    def __str__(self):
        return self.name


class LevelsGroup(models.Model):
    units = models.ForeignKey('Units', models.CASCADE)
    description = models.CharField(max_length=145, blank=True, null=True)
    level = models.ManyToManyField('Level', through='LevelsGroupHasLevel')

    class Meta:
        managed = False
        db_table = 'levels_group'

    def __str__(self):
        return self.description

class LevelsGroupHasLevel(models.Model):
    levels_group = models.ForeignKey('LevelsGroup', models.CASCADE)
    level = models.ForeignKey('Level', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'levels_group_has_level'
        unique_together = (('levels_group', 'level'),)


class Option(models.Model):
    gui_element = models.ForeignKey('GuiElement', models.CASCADE, blank=True, null=True)
    label = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'option'

    def __str__(self):
        return self.label


class OptionValue(models.Model):
    label = models.CharField(max_length=145, blank=True, null=True)
    language = models.ManyToManyField('Language', through='OptionValueI18N')

    class Meta:
        managed = False
        db_table = 'option_value'

    def __str__(self):
        return self.label


class OptionValueI18N(models.Model):
    option_value = models.ForeignKey('OptionValue', models.CASCADE)
    language = models.ForeignKey(Language, models.CASCADE)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'option_value_i18n'
        unique_together = (('option_value', 'language'), ('language', 'name'),)

    def __str__(self):
        return self.name


class OptionsOverride(models.Model):
    arguments_group_has_processor = models.ForeignKey('ArgumentsGroupHasProcessor', models.CASCADE)
    option = models.ForeignKey('Option', models.CASCADE)
    option_value = models.ForeignKey('OptionValue', models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'options_override'
        unique_together = (('arguments_group_has_processor', 'option'),)


class Organization(models.Model):
    url = models.CharField(max_length=45, blank=True, null=True)
    language = models.ManyToManyField('Language', through='OrganizationI18N')

    class Meta:
        managed = False
        db_table = 'organization'


class OrganizationI18N(models.Model):
    organization = models.ForeignKey('Organization', models.CASCADE)
    language = models.ForeignKey('Language', models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organization_i18n'
        unique_together = (('organization', 'language'), ('name', 'language'),)

    def __str__(self):
        return self.name


class Parameter(models.Model):
    accumulation_mode = models.ForeignKey('AccumulationMode', models.CASCADE)
    is_visible = models.IntegerField(blank=True, null=True, default=1)
    language = models.ManyToManyField('Language', through='ParameterI18N')

    class Meta:
        managed = False
        db_table = 'parameter'


class ParameterI18N(models.Model):
    name = models.CharField(max_length=200, blank=True, null=False)
    language = models.ForeignKey('Language', models.CASCADE)
    parameter = models.ForeignKey('Parameter', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'parameter_i18n'
        unique_together = (('language', 'parameter'), ('name', 'language'),)

    def __str__(self):
        return self.name


class Processor(models.Model):
    is_visible = models.IntegerField()
    arguments_selected_by_user = models.IntegerField(blank=True, null=True)
    conveyor = models.ForeignKey('Conveyor', models.CASCADE, blank=True, null=True)
    arguments_group = models.ManyToManyField('ArgumentsGroup', through='ProcessorHasArguments', related_name='arguments_group')
    language = models.ManyToManyField('Language', through='ProcessorI18N')
    option = models.ManyToManyField('Option', through='ProcessorHasOptions')
    time_period_type = models.ManyToManyField('TimePeriodType', through='ProcessorHasTimePeriodType')

    class Meta:
        managed = False
        db_table = 'processor'


class ProcessorHasArguments(models.Model):
    processor = models.ForeignKey('Processor', models.CASCADE)
    arguments_group = models.ForeignKey('ArgumentsGroup', models.CASCADE)
    argument_position = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'processor_has_arguments'
        unique_together = (('processor', 'arguments_group', 'argument_position'),)


class ProcessorHasOptions(models.Model):
    processor = models.ForeignKey('Processor', models.CASCADE)
    option = models.ForeignKey('Option', models.CASCADE)
    option_value = models.ForeignKey('OptionValue', models.CASCADE)
    condition = models.ForeignKey('self', models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'processor_has_options'
        unique_together = (('processor', 'option', 'option_value'),)


class ProcessorHasTimePeriodType(models.Model):
    processor = models.ForeignKey('Processor', models.CASCADE)
    time_period_type = models.ForeignKey('TimePeriodType', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'processor_has_time_period_type'
        unique_together = (('processor', 'time_period_type'),)


class ProcessorI18N(models.Model):
    processor = models.ForeignKey('Processor', models.CASCADE)
    language = models.ForeignKey('Language', models.CASCADE)
    name = models.CharField(max_length=145, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    reference = models.CharField(max_length=245, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'processor_i18n'
        unique_together = (('processor', 'language'), ('name', 'language'),)

    def __str__(self):
        return self.name


class Property(models.Model):
    label = models.CharField(max_length=145, blank=True, null=True)
    gui_element = models.ForeignKey('GuiElement', models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property'

    def __str__(self):
        return self.label if self.label is not None else ''


class PropertyValue(models.Model):
    label = models.CharField(max_length=145, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'property_value'

    def __str__(self):
        return self.label if self.label is not None else ''

class Resolution(models.Model):
    name = models.CharField(unique=True, max_length=45)
    subpath1 = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'resolution'

    def __str__(self):
        return self.name


class RootDir(models.Model):
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'root_dir'

    def __str__(self):
        return self.name


class Scenario(models.Model):
    name = models.CharField(unique=True, max_length=45, blank=True, null=True)
    subpath0 = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scenario'

    def __str__(self):
        return self.name


class SpecificParameter(models.Model):
    parameter = models.ForeignKey('Parameter', models.CASCADE)
    levels_group = models.ForeignKey('LevelsGroup', models.CASCADE)
    time_step = models.ForeignKey('TimeStep', models.CASCADE)
    arguments_group = models.ManyToManyField('ArgumentsGroup', through='ArgumentsGroupHasSpecificParameter')

    class Meta:
        managed = False
        db_table = 'specific_parameter'


class TimePeriodType(models.Model):
    const_name = models.CharField(unique=True, max_length=45)
    language = models.ManyToManyField('Language', through='TimePeriodTypeI18N')

    class Meta:
        managed = False
        db_table = 'time_period_type'


class TimePeriodTypeI18N(models.Model):
    time_period_type = models.ForeignKey('TimePeriodType', models.CASCADE)
    language = models.ForeignKey('Language', models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'time_period_type_i18n'
        unique_together = (('time_period_type', 'language'), ('language', 'name'),)

    def __str__(self):
        return self.name


class TimeStep(models.Model):
    label = models.CharField(unique=True, max_length=45)
    subpath2 = models.CharField(max_length=45, blank=True, null=True)
    language = models.ManyToManyField('Language', through='TimeStepI18N')

    class Meta:
        managed = False
        db_table = 'time_step'


class TimeStepI18N(models.Model):
    time_step = models.ForeignKey('TimeStep', models.CASCADE)
    language = models.ForeignKey('Language', models.CASCADE)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'time_step_i18n'
        unique_together = (('time_step', 'language'), ('name', 'language'),)

    def __str__(self):
        return self.name


class Units(models.Model):
    language = models.ManyToManyField('Language', through='UnitsI18N')

    class Meta:
        managed = False
        db_table = 'units'


class UnitsI18N(models.Model):
    units = models.ForeignKey('Units', models.CASCADE)
    language = models.ForeignKey('Language', models.CASCADE)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'units_i18n'
        unique_together = (('units', 'language'),)

    def __str__(self):
        return self.name


class Variable(models.Model):
    name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'variable'

    def __str__(self):
        return self.name

class Vertex(models.Model):
    computing_module = models.ForeignKey('ComputingModule', models.CASCADE)
    condition_option = models.ForeignKey('Option', models.CASCADE, blank=True, null=True)
    condition_value = models.ForeignKey('OptionValue', models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vertex'
