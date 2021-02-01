from rest_framework import serializers
from rest_framework.reverse import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from collections import OrderedDict
from rest_framework.renderers import *

from .models import *


class ModifiedRelatedField(serializers.RelatedField):

    # Below code is copied from rest_framework.serializers.RelatedField
    # because we need to override the keys in the return value
    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            # Ensure that field.choices returns something sensible
            # even when accessed with a read-only field.
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                # This is the only line that differs
                # from the RelatedField's implementation
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])


class OrganizationI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationI18N
        fields = ['id', 'name']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Organization name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    organizationi18n = OrganizationI18NSerializer(source='organizationi18n_set', label='')
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:organization-detail',
                                                   read_only=True)
    class Meta:
        model = Organization
        fields = ['id', 'dataurl', 'organizationi18n', 'url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['url'].label = _('Organization URL')
        self.fields['url'].style = {'template': 'metadb/custom_input.html'}


    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        organizationi18n_data = validated_data.pop('organizationi18n_set')
        organization = Organization.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            OrganizationI18N.objects.create(organization=organization,
                                            language=db_lang,
                                            **organizationi18n_data)

        return organization

    def update(self, instance, validated_data):
        instance.url = validated_data.get('url', instance.url)
        organizationi18n = instance.organizationi18n_set.filter(language__code=get_language()).get()
        organizationi18n.name = validated_data['organizationi18n_set'].get('name', organizationi18n.name)
        organizationi18n.save()
        instance.save()

        return instance


class OrganizationRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = OrganizationSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return Organization.objects.get(pk=data)


class CollectionI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollectionI18N
        fields = ['id', 'name', 'description']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Collection name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}
        self.fields['description'].label = _('Collection description')
        self.fields['description'].style = {'template': 'metadb/custom_textarea.html', 'rows': 3}


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    collectioni18n = CollectionI18NSerializer(source='collectioni18n_set', label='')
    qset = Organization.objects.order_by('organizationi18n__name')
    organization = OrganizationRelatedField(queryset=qset)
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:collection-detail',
                                                   read_only=True)
    class Meta:
        model = Collection
        fields = ['id', 'dataurl', 'label', 'url', 'collectioni18n', 'organization']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['label'].label = _('Collection label')
        self.fields['label'].style = {'template': 'metadb/custom_input.html'}
        self.fields['url'].label = _('Collection URL')
        self.fields['url'].style = {'template': 'metadb/custom_input.html'}
        self.fields['organization'].label = _('Organization')
        self.fields['organization'].data_url = reverse('metadb:organization-list')
        self.fields['organization'].widget_type = 'select'
        self.fields['organization'].style = {'template': 'metadb/custom_select.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        collectioni18n_data = validated_data.pop('collectioni18n_set')
        collection = Collection.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            CollectionI18N.objects.create(collection=collection,
                                          language=db_lang,
                                          **collectioni18n_data)

        return collection

    def update(self, instance, validated_data):
        instance.label = validated_data.get('label', instance.label)
        instance.url = validated_data.get('url', instance.url)
        collectioni18n = instance.collectioni18n_set.filter(language__code=get_language()).get()
        collectioni18n.name = validated_data['collectioni18n_set'].get('name', collectioni18n.name)
        collectioni18n.description = validated_data['collectioni18n_set'].get('description', collectioni18n.description)
        collectioni18n.save()
        instance.organization = validated_data.get('organization', instance.organization)
        instance.save()

        return instance


class CollectionRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = CollectionSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data['label']
        if action == 'update':
            result = data.get('id', None)
        return result

    def to_internal_value(self, data):
        return Collection.objects.get(pk=data)


class ScenarioSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:scenario-detail',
                                                   read_only=True)
    class Meta:
        model = Scenario
        fields = ['id', 'dataurl', 'name', 'subpath0']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Scenario name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}
        self.fields['subpath0'].label = _('Scenario subpath')
        self.fields['subpath0'].style = {'template': 'metadb/custom_input.html'}


    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Scenario.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.subpath0 = validated_data.get('subpath0', instance.subpath0)
        instance.save()
        return instance


class ScenarioRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = ScenarioSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data['name']
        if action == 'update':
            result = data.get('id', None)
        return result

    def to_internal_value(self, data):
        return Scenario.objects.get(pk=data)


class ResolutionSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:resolution-detail',
                                                   read_only=True)
    class Meta:
        model = Resolution
        fields = ['id', 'dataurl', 'name', 'subpath1']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Resolution name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}
        self.fields['subpath1'].label = _('Resolution subpath')
        self.fields['subpath1'].style = {'template': 'metadb/custom_input.html'}


    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Resolution.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.subpath1 = validated_data.get('subpath1', instance.subpath1)
        instance.save()
        return instance


class ResolutionRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = ResolutionSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data['name']
        if action == 'update':
            result = data.get('id', None)
        return result

    def to_internal_value(self, data):
        return Resolution.objects.get(pk=data)


class DataKindSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:datakind-detail',
                                                   read_only=True)
    class Meta:
        model = DataKind
        fields = ['id', 'dataurl', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Data kind name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return DataKind.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class DataKindRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = DataKindSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data['name']
        if action == 'update':
            result = data.get('id', None)
        return result

    def to_internal_value(self, data):
        return DataKind.objects.get(pk=data)


class FileTypeSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:filetype-detail',
                                                   read_only=True)
    class Meta:
        model = FileType
        fields = ['id', 'dataurl', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('File type name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return FileType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class FileTypeRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = FileTypeSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data['name']
        if action == 'update':
            result = data.get('id', None)
        return result

    def to_internal_value(self, data):
        return FileType.objects.get(pk=data)


class DatasetSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:dataset-detail',
                                                   read_only=True)
    qset = Collection.objects.order_by('collectioni18n__name')
    collection_label = CollectionRelatedField(queryset=qset, source='collection')
    qset = Scenario.objects.order_by('name')
    scenario_name = ScenarioRelatedField(queryset=qset, source='scenario')
    qset = Resolution.objects.order_by('name')
    resolution_name = ResolutionRelatedField(queryset=qset, source='resolution')
    qset = DataKind.objects.order_by('name')
    data_kind_name = DataKindRelatedField(queryset=qset, source='data_kind')
    qset = FileType.objects.order_by('name')
    file_type_name = FileTypeRelatedField(queryset=qset, source='file_type')
    class Meta:
        model = Dataset
        fields = ['id', 'dataurl', 'is_visible', 'collection_label', 'resolution_name',
                  'scenario_name', 'data_kind_name', 'file_type_name', 'time_start',
                  'time_end', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Is visible
        self.fields['is_visible'].label = _('Visible')
        self.fields['is_visible'].style = {'template': 'metadb/custom_checkbox.html'}
        self.fields['is_visible'].initial = True
        # Collection label
        self.fields['collection_label'].data_url = reverse('metadb:collection-list')
        self.fields['collection_label'].label = _('Collection label')
        self.fields['collection_label'].style = {'template': 'metadb/custom_select.html'}
        self.fields['collection_label'].widget_type = 'select'
        # Horizontal resolution
        self.fields['resolution_name'].data_url = reverse('metadb:resolution-list')
        self.fields['resolution_name'].label = _('Horizontal resolution')
        self.fields['resolution_name'].style = {'template': 'metadb/custom_select.html'}
        self.fields['resolution_name'].widget_type = 'select'
        # Scenario
        self.fields['scenario_name'].data_url = reverse('metadb:scenario-list')
        self.fields['scenario_name'].label = _('Scenario')
        self.fields['scenario_name'].style = {'template': 'metadb/custom_select.html'}
        self.fields['scenario_name'].widget_type = 'select'
        # Data kind
        self.fields['data_kind_name'].data_url = reverse('metadb:datakind-list')
        self.fields['data_kind_name'].label = _('Data kind')
        self.fields['data_kind_name'].style = {'template': 'metadb/custom_select.html'}
        self.fields['data_kind_name'].widget_type = 'select'
        # File type
        self.fields['file_type_name'].data_url = reverse('metadb:filetype-list')
        self.fields['file_type_name'].label = _('File type')
        self.fields['file_type_name'].style = {'template': 'metadb/custom_select.html'}
        self.fields['file_type_name'].widget_type = 'select'
        # Time start
        self.fields['time_start'].label = _('Start date')
        self.fields['time_start'].style = {'template': 'metadb/custom_input.html'}
        # Time end
        self.fields['time_end'].label = _('End date')
        self.fields['time_end'].style = {'template': 'metadb/custom_input.html'}
        # Description
        self.fields['description'].label = _('Description')
        self.fields['description'].style = {'template': 'metadb/custom_textarea.html', 'rows': 3}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Dataset.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.is_visible = validated_data.get('is_visible', instance.is_visible)
        instance.collection = validated_data.get('collection', instance.collection)
        instance.resolution = validated_data.get('resolution', instance.resolution)
        instance.scenario = validated_data.get('scenario', instance.scenario)
        instance.data_kind = validated_data.get('data_kind', instance.data_kind)
        instance.file_type = validated_data.get('file_type', instance.file_type)
        instance.time_start = validated_data.get('time_start', instance.time_start)
        instance.time_end = validated_data.get('time_end', instance.time_end)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance


class AccumulationModeSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:accumulationmode-detail',
                                                   read_only=True)
    class Meta:
        model = AccumulationMode
        fields = ['id', 'dataurl', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Accumulation mode')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return AccumulationMode.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class AccumulationModeRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = AccumulationModeSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data['name']
        if action == 'update':
            result = data.get('id', None)
        return result

    def to_internal_value(self, data):
        return AccumulationMode.objects.get(pk=data)

class ParameterI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParameterI18N
        fields = ['id', 'name']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Parameter name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


class ParameterSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:parameter-detail',
                                                   read_only=True)
    qset = AccumulationMode.objects.order_by('name')
    accumulation_mode = AccumulationModeRelatedField(queryset=qset)
    parameteri18n = ParameterI18NSerializer(source='parameteri18n_set', label='')

    class Meta:
        model = Parameter
        fields = ['id', 'dataurl', 'is_visible', 'accumulation_mode', 'parameteri18n']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Is visible
        self.fields['is_visible'].label = _('Visible')
        self.fields['is_visible'].style = {'template': 'metadb/custom_checkbox.html'}
        self.fields['is_visible'].initial = True
        # Accumulation mode
        self.fields['accumulation_mode'].data_url = reverse('metadb:accumulationmode-list')
        self.fields['accumulation_mode'].label = _('Accumulation mode')
        self.fields['accumulation_mode'].style = {'template': 'metadb/custom_select.html'}
        self.fields['accumulation_mode'].widget_type = 'select'

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        parameteri18n_data = validated_data.pop('parameteri18n_set')
        parameter = Parameter.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            ParameterI18N.objects.create(parameter=parameter,
                                          language=db_lang,
                                          **parameteri18n_data)

        return parameter

    def update(self, instance, validated_data):
        instance.is_visible = validated_data.get('is_visible', instance.is_visible)
        instance.accumulation_mode = validated_data.get('accumulation_mode', instance.accumulation_mode)
        parameteri18n = instance.parameteri18n_set.filter(language__code=get_language()).get()
        parameteri18n.name = validated_data['parameteri18n_set'].get('name', parameteri18n.name)
        parameteri18n.save()
        instance.save()

        return instance


class ParameterRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = ParameterSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return Parameter.objects.get(pk=data)


class UnitsI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnitsI18N
        fields = ['id', 'name']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Measurement unit name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


class UnitsSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:organization-detail',
                                                   read_only=True)
    unitsi18n = UnitsI18NSerializer(source='unitsi18n_set', label='')

    class Meta:
        model = Units
        fields = ['id', 'dataurl', 'unitsi18n']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        unitsi18n_data = validated_data.pop('unitsi18n_set')
        units = Units.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            UnitsI18N.objects.create(units=units,
                                     language=db_lang,
                                     **unitsi18n_data)

        return units

    def update(self, instance, validated_data):
        unitsi18n = instance.unitsi18n_set.filter(language__code=get_language()).get()
        unitsi18n.name = validated_data['unitsi18n_set'].get('name', unitsi18n.name)
        unitsi18n.save()
        instance.save()

        return instance


class UnitsRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = UnitsSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return Units.objects.get(pk=data)


class LevelI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = LevelI18N
        fields = ['id', 'name']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Level name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


class LevelSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:level-detail',
                                                   read_only=True)
    leveli18n = LevelI18NSerializer(source='leveli18n_set', label='')

    class Meta:
        model = Level
        fields = ['id', 'dataurl', 'label', 'leveli18n']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['label'].label = _('Level label')
        self.fields['label'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        leveli18n_data = validated_data.pop('leveli18n_set')
        level = Level.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            LevelI18N.objects.create(level=level,
                                     language=db_lang,
                                     **leveli18n_data)

        return level

    def update(self, instance, validated_data):
        leveli18n = instance.leveli18n_set.filter(language__code=get_language()).get()
        leveli18n.name = validated_data['leveli18n_set'].get('name', leveli18n.name)
        leveli18n.save()
        instance.label = validated_data.get('label', instance.label)
        instance.save()

        return instance


class LevelRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = LevelSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return Level.objects.get(pk=data)


class LevelsGroupSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:levelsgroup-detail',
                                                   read_only=True)
    qset = Units.objects.order_by('unitsi18n__name')
    units = UnitsRelatedField(queryset=qset)
    qset = Level.objects.order_by('leveli18n__name')
    levels = LevelRelatedField(queryset=qset, many=True, source='level')

    class Meta:
        model = LevelsGroup
        fields = ['id', 'dataurl', 'description', 'units', 'levels']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Description
        self.fields['description'].label = _('Description')
        self.fields['description'].style = {'template': 'metadb/custom_input.html'}
        # Units
        self.fields['units'].data_url = reverse('metadb:units-list')
        self.fields['units'].label = _('Measurement units')
        self.fields['units'].style = {'template': 'metadb/custom_select.html'}
        # Level
        self.fields['levels'].data_url = reverse('metadb:level-list')
        self.fields['levels'].label = _('Levels')
        self.fields['levels'].style = {'template': 'metadb/custom_select_multiple.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        levelslist = validated_data.pop('level')
        levelsgroup = LevelsGroup.objects.create(**validated_data)
        levelsgroup.level.set(levelslist)
        return levelsgroup

    def update(self, instance, validated_data):
        instance.units = validated_data.get('units', instance.units)
        instance.description = validated_data.get('description', instance.description)
        levelslist = validated_data.get('level', instance.level)
        instance.level.set(levelslist)
        instance.save()

        return instance


class LevelsGroupRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = LevelsGroupSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return LevelsGroup.objects.get(pk=data)


class TimeStepI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeStepI18N
        fields = ['id', 'name']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('Time step name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}


class TimeStepSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:timestep-detail',
                                                   read_only=True)
    timestepi18n = TimeStepI18NSerializer(source='timestepi18n_set', label='')

    class Meta:
        model = TimeStep
        fields = ['id', 'dataurl', 'label', 'timestepi18n', 'subpath2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['label'].label = _('Time step label')
        self.fields['label'].style = {'template': 'metadb/custom_input.html'}
        self.fields['subpath2'].label = _('Time step subpath')
        self.fields['subpath2'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        timestepi18n_data = validated_data.pop('timestepi18n_set')
        timestep = TimeStep.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            TimeStepI18N.objects.create(time_step=timestep,
                                        language=db_lang,
                                        **timestepi18n_data)

        return timestep

    def update(self, instance, validated_data):
        timestepi18n = instance.timestepi18n_set.filter(language__code=get_language()).get()
        timestepi18n.name = validated_data['timestepi18n_set'].get('name', timestepi18n.name)
        timestepi18n.save()
        instance.save()

        return instance


class TimeStepRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = TimeStepSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return TimeStep.objects.get(pk=data)



class SpecificParameterSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:specificparameter-detail',
                                                   read_only=True)
    qset = Parameter.objects.order_by('parameteri18n__name')
    parameter = ParameterRelatedField(queryset=qset)
    qset = LevelsGroup.objects.all()
    levels_group = LevelsGroupRelatedField(queryset=qset)
    qset = TimeStep.objects.all()
    time_step = TimeStepRelatedField(queryset=qset)

    class Meta:
        model = SpecificParameter
        fields = ['id', 'dataurl', 'parameter', 'levels_group', 'time_step']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Parameter
        self.fields['parameter'].data_url = reverse('metadb:parameter-list')
        self.fields['parameter'].label = _('Meteorological parameter')
        self.fields['parameter'].style = {'template': 'metadb/custom_select.html'}
        self.fields['parameter'].widget_type = 'select'
        # Parameter
        self.fields['levels_group'].data_url = reverse('metadb:levelsgroup-list')
        self.fields['levels_group'].label = _('Levels group')
        self.fields['levels_group'].style = {'template': 'metadb/custom_select.html'}
        self.fields['levels_group'].widget_type = 'select'
        # Parameter
        self.fields['time_step'].data_url = reverse('metadb:timestep-list')
        self.fields['time_step'].label = _('Time step')
        self.fields['time_step'].style = {'template': 'metadb/custom_select.html'}
        self.fields['time_step'].widget_type = 'select'


    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Dataset.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.is_visible = validated_data.get('is_visible', instance.is_visible)
        instance.collection = validated_data.get('collection', instance.collection)
        instance.resolution = validated_data.get('resolution', instance.resolution)
        instance.scenario = validated_data.get('scenario', instance.scenario)
        instance.data_kind = validated_data.get('data_kind', instance.data_kind)
        instance.file_type = validated_data.get('file_type', instance.file_type)
        instance.time_start = validated_data.get('time_start', instance.time_start)
        instance.time_end = validated_data.get('time_end', instance.time_end)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance