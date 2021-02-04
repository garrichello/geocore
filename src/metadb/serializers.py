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
        self.fields['organization'].style = {'template': 'metadb/custom_select.html'}
        self.fields['organization'].allow_blank = True

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
        result = data
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
        result = data
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
    qset = Collection.objects.order_by('label')
    collection_label = CollectionRelatedField(queryset=qset, source='collection')
    qset = Scenario.objects.order_by('name')
    scenario = ScenarioRelatedField(queryset=qset)
    qset = Resolution.objects.order_by('name')
    resolution = ResolutionRelatedField(queryset=qset)
    qset = DataKind.objects.order_by('name')
    data_kind_name = DataKindRelatedField(queryset=qset, source='data_kind')
    qset = FileType.objects.order_by('name')
    file_type_name = FileTypeRelatedField(queryset=qset, source='file_type')
    class Meta:
        model = Dataset
        fields = ['id', 'dataurl', 'is_visible', 'collection_label', 'resolution',
                  'scenario', 'data_kind_name', 'file_type_name', 'time_start',
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
        self.fields['collection_label'].allow_blank = True
        # Horizontal resolution
        self.fields['resolution'].data_url = reverse('metadb:resolution-list')
        self.fields['resolution'].label = _('Horizontal resolution')
        self.fields['resolution'].style = {'template': 'metadb/custom_select.html'}
        self.fields['resolution'].allow_blank = True
        # Scenario
        self.fields['scenario'].data_url = reverse('metadb:scenario-list')
        self.fields['scenario'].label = _('Scenario')
        self.fields['scenario'].style = {'template': 'metadb/custom_select.html'}
        self.fields['scenario'].allow_blank = True
        # Data kind
        self.fields['data_kind_name'].data_url = reverse('metadb:datakind-list')
        self.fields['data_kind_name'].label = _('Data kind')
        self.fields['data_kind_name'].style = {'template': 'metadb/custom_select.html'}
        self.fields['data_kind_name'].allow_blank = True
        # File type
        self.fields['file_type_name'].data_url = reverse('metadb:filetype-list')
        self.fields['file_type_name'].label = _('File type')
        self.fields['file_type_name'].style = {'template': 'metadb/custom_select.html'}
        self.fields['file_type_name'].allow_blank = True
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


class DatasetRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = DatasetSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = data.get('id', None)
        return result

    def to_internal_value(self, data):
        return Dataset.objects.get(pk=data)

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
        self.fields['accumulation_mode'].allow_blank = True

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
        self.fields['units'].allow_blank = True
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
        fields = ['id', 'dataurl', 'label', 'subpath2', 'timestepi18n']

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

        return timesteps

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
        fields = ['id', 'dataurl', 'parameter', 'time_step', 'levels_group']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Parameter
        self.fields['parameter'].data_url = reverse('metadb:parameter-list')
        self.fields['parameter'].label = _('Meteorological parameter')
        self.fields['parameter'].style = {'template': 'metadb/custom_select.html'}
        self.fields['parameter'].allow_blank = True
        # Levels group
        self.fields['levels_group'].data_url = reverse('metadb:levelsgroup-list')
        self.fields['levels_group'].label = _('Levels group')
        self.fields['levels_group'].style = {'template': 'metadb/custom_select.html'}
        self.fields['levels_group'].allow_blank = True
        # Time step
        self.fields['time_step'].data_url = reverse('metadb:timestep-list')
        self.fields['time_step'].label = _('Time step')
        self.fields['time_step'].style = {'template': 'metadb/custom_select.html'}
        self.fields['time_step'].allow_blank = True


    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return SpecificParameter.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.parameter = validated_data.get('parameter', instance.parameter)
        instance.levels_group = validated_data.get('levels_group', instance.levels_group)
        instance.time_step = validated_data.get('time_step', instance.time_step)
        instance.save()

        return instance

class SpecificParameterRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = SpecificParameterSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return SpecificParameter.objects.get(pk=data)


class GuiElementI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = GuiElementI18N
        fields = ['id', 'caption']

    def to_representation(self, instance):
        data = instance.filter(language__code=get_language()).get()
        return super().to_representation(data)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['caption'].label = _('GUI element caption')
        self.fields['caption'].style = {'template': 'metadb/custom_input.html'}


class GuiElementSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:guielement-detail',
                                                   read_only=True)
    guielementi18n = GuiElementI18NSerializer(source='guielementi18n_set', label='')

    class Meta:
        model = GuiElement
        fields = ['id', 'dataurl', 'name', 'guielementi18n']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = _('GUI element name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        guielementi18n_data = validated_data.pop('guielementi18n_set')
        guielement = GuiElement.objects.create(**validated_data)
        for db_lang in Language.objects.all():
            GuiElementI18N.objects.create(gui_element=guielement,
                                          language=db_lang,
                                          **guielementi18n_data)

        return guielement

    def update(self, instance, validated_data):
        guielementi18n = instance.guielementi18n_set.filter(language__code=get_language()).get()
        guielementi18n.caption = validated_data['guielementi18n_set'].get('caption', guielementi18n.caption)
        guielementi18n.save()
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance


class GuiElementRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = GuiElementSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return GuiElement.objects.get(pk=data)


class PropertySerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:property-detail',
                                                   read_only=True)
    qset = GuiElement.objects.order_by('name')
    gui_element = GuiElementRelatedField(queryset=qset)

    class Meta:
        model = Property
        fields = ['id', 'dataurl', 'label', 'gui_element']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['label'].label = _('Property label')
        self.fields['label'].style = {'template': 'metadb/custom_input.html'}
        # GUI element
        self.fields['gui_element'].data_url = reverse('metadb:guielement-list')
        self.fields['gui_element'].label = _('GUI element name')
        self.fields['gui_element'].style = {'template': 'metadb/custom_select.html'}
        self.fields['gui_element'].allow_blank = True

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Property.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.label = validated_data.get('label', instance.label)
        instance.gui_element = validated_data.get('gui_element', instance.gui_element)
        instance.save()

        return instance


class PropertyRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = PropertySerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return Property.objects.get(pk=data)


class PropertyValueSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:propertyvalue-detail',
                                                   read_only=True)
    class Meta:
        model = Property
        fields = ['id', 'dataurl', 'label']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['label'].label = _('Property value label')
        self.fields['label'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Property.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.label = validated_data.get('label', instance.label)
        instance.save()

        return instance


class PropertyValueRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = PropertyValueSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return PropertyValue.objects.get(pk=data)


class VariableSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:variable-detail',
                                                   read_only=True)
    class Meta:
        model = Variable
        fields = ['id', 'dataurl', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['name'].label = _('Variable name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Variable.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance


class VariableRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = VariableSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return Variable.objects.get(pk=data)


class LevelsVariableSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:levelsvariable-detail',
                                                   read_only=True)
    class Meta:
        model = Variable
        fields = ['id', 'dataurl', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['name'].label = _('Levels variable name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Variable.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance


class LevelsVariableRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = VariableSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return Variable.objects.get(pk=data)


class FileSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:file-detail',
                                                   read_only=True)
    class Meta:
        model = File
        fields = ['id', 'dataurl', 'name_pattern']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['name_pattern'].label = _('File name pattern')
        self.fields['name_pattern'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return File.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name_pattern = validated_data.get('name_pattern', instance.name_pattern)
        instance.save()

        return instance


class FileRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = FileSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return File.objects.get(pk=data)


class RootDirSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:rootdir-detail',
                                                   read_only=True)
    class Meta:
        model = RootDir
        fields = ['id', 'dataurl', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Label
        self.fields['name'].label = _('Root directory name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return RootDir.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        return instance


class RootDirRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = RootDirSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return RootDir.objects.get(pk=data)


class DataSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:data-detail',
                                                   read_only=True)
    qset = Dataset.objects.all().order_by('description')
    dataset = DatasetRelatedField(queryset=qset)
#    qset = SpecificParameter.objects.all()
#    specific_parameter = SpecificParameterRelatedField(queryset=qset)
    qset = Parameter.objects.all().order_by('parameteri18n__name')
    parameter = ParameterRelatedField(queryset=qset, source='specific_parameter.parameter')
    qset = LevelsGroup.objects.all()
    levels_group = LevelsGroupRelatedField(queryset=qset, source='specific_parameter.levels_group')
    qset = TimeStep.objects.all().order_by('timestepi18n__name')
    time_step = TimeStepRelatedField(queryset=qset, source='specific_parameter.time_step')
    qset = Property.objects.all()
    property = PropertyRelatedField(queryset=qset)
    qset = PropertyValue.objects.all()
    property_value = PropertyValueRelatedField(queryset=qset)
    qset = Units.objects.order_by('unitsi18n__name')
    units = UnitsRelatedField(queryset=qset)
    qset = Variable.objects.all()
    variable = VariableRelatedField(queryset=qset)
    qset = File.objects.all()
    file = FileRelatedField(queryset=qset)
    qset = Variable.objects.all()
    levels_variable = VariableRelatedField(queryset=qset)
    qset = RootDir.objects.all()
    root_dir = RootDirRelatedField(queryset=qset)

    class Meta:
        model = Data
        fields = ['id', 'dataurl', 'dataset', 'parameter', 'time_step', 'levels_group', 
                  'variable', 'units', 'levels_variable', 'property', 'property_value', 
                  'file', 'root_dir', 'scale', 'offset']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dataset
        self.fields['dataset'].data_url = reverse('metadb:dataset-list')
        self.fields['dataset'].label = _('Dataset')
        self.fields['dataset'].style = {'template': 'metadb/custom_select.html'}
        self.fields['dataset'].allow_blank = True
        # Specific parameter
#        self.fields['specific_parameter'].data_url = reverse('metadb:specificparameter-list')
#        self.fields['specific_parameter'].label = _('Specific parameter')
#        self.fields['specific_parameter'].style = {'template': 'metadb/custom_select.html'}
#        self.fields['specific_parameter'].allow_blank = True
        # Parameter
        self.fields['parameter'].data_url = reverse('metadb:parameter-list')
        self.fields['parameter'].label = _('Meteorological parameter')
        self.fields['parameter'].style = {'template': 'metadb/custom_select.html'}
        self.fields['parameter'].allow_blank = True
        self.fields['parameter'].no_add_btn = True
        # Levels group
        self.fields['levels_group'].data_url = reverse('metadb:levelsgroup-list')
        self.fields['levels_group'].label = _('Levels group')
        self.fields['levels_group'].style = {'template': 'metadb/custom_select.html'}
        self.fields['levels_group'].allow_blank = True
        self.fields['levels_group'].no_add_btn = True
        # Time step
        self.fields['time_step'].data_url = reverse('metadb:timestep-list')
        self.fields['time_step'].label = _('Time step')
        self.fields['time_step'].style = {'template': 'metadb/custom_select.html'}
        self.fields['time_step'].allow_blank = True
        self.fields['time_step'].no_add_btn = True
        # Property
        self.fields['property'].data_url = reverse('metadb:property-list')
        self.fields['property'].label = _('Property')
        self.fields['property'].style = {'template': 'metadb/custom_select.html'}
        self.fields['property'].allow_blank = True
        # Property value
        self.fields['property_value'].data_url = reverse('metadb:propertyvalue-list')
        self.fields['property_value'].label = _('Property value')
        self.fields['property_value'].style = {'template': 'metadb/custom_select.html'}
        self.fields['property_value'].allow_blank = True
        # Units
        self.fields['units'].data_url = reverse('metadb:units-list')
        self.fields['units'].label = _('Units')
        self.fields['units'].style = {'template': 'metadb/custom_select.html'}
        self.fields['units'].allow_blank = True
        # Variable
        self.fields['variable'].data_url = reverse('metadb:variable-list')
        self.fields['variable'].label = _('Variable')
        self.fields['variable'].style = {'template': 'metadb/custom_select.html'}
        self.fields['variable'].allow_blank = True
        # File
        self.fields['file'].data_url = reverse('metadb:file-list')
        self.fields['file'].label = _('File name pattern')
        self.fields['file'].style = {'template': 'metadb/custom_select.html'}
        self.fields['file'].allow_blank = True
        # Levels variable
        self.fields['levels_variable'].data_url = reverse('metadb:levelsvariable-list')
        self.fields['levels_variable'].label = _('Levels variable')
        self.fields['levels_variable'].style = {'template': 'metadb/custom_select.html'}
        self.fields['levels_variable'].allow_blank = True
        # Root directory
        self.fields['root_dir'].data_url = reverse('metadb:rootdir-list')
        self.fields['root_dir'].label = _('Root directory')
        self.fields['root_dir'].style = {'template': 'metadb/custom_select.html'}
        self.fields['root_dir'].allow_blank = True
        # Scale
        self.fields['scale'].label = _('Scale coefficient')
        self.fields['scale'].style = {'template': 'metadb/custom_input.html'}
        self.fields['scale'].initial = 1.0
        # Offset
        self.fields['offset'].label = _('Offset coefficient')
        self.fields['offset'].style = {'template': 'metadb/custom_input.html'}
        self.fields['offset'].initial = 0.0


    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        specific_parameter_data = validated_data.pop('specific_parameter')
        specific_parameter = SpecificParameter.objects.filter(
            parameter=specific_parameter_data['parameter'],
            time_step=specific_parameter_data['time_step'],
            levels_group=specific_parameter_data['levels_group']
        ).get()
        data = Data.objects.create(**validated_data, specific_parameter = specific_parameter)
        return data

    def update(self, instance, validated_data):
        instance.dataset = validated_data.get('dataset', instance.dataset)
        specific_parameter_data = validated_data.get('specific_parameter')
        specific_parameter = SpecificParameter.objects.filter(
            parameter=specific_parameter_data['parameter'],
            time_step=specific_parameter_data['time_step'],
            levels_group=specific_parameter_data['levels_group']
        ).get()
        instance.specific_parameter = specific_parameter
        instance.property = validated_data.get('property', instance.property)
        instance.property_value = validated_data.get('property_value', instance.property_value)
        instance.units = validated_data.get('units', instance.units)
        instance.variable = validated_data.get('variable', instance.variable)
        instance.file = validated_data.get('file', instance.file)
        instance.levels_variable = validated_data.get('levels_variable', instance.levels_variable)
        instance.root_dir = validated_data.get('root_dir', instance.root_dir)
        instance.scale = validated_data.get('scale', instance.scale)
        instance.offset = validated_data.get('offset', instance.offset)
        instance.save()

        return instance


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:language-detail',
                                                   read_only=True)
    class Meta:
        model = Language
        fields = ['id', 'dataurl', 'name', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Name
        self.fields['name'].label = _('Language name')
        self.fields['name'].style = {'template': 'metadb/custom_input.html'}
        # Code
        self.fields['code'].label = _('Language code')
        self.fields['code'].style = {'template': 'metadb/custom_input.html'}

    def to_representation(self, instance):
        action = self.context['request'].META.get('HTTP_ACTION')
        if action == 'options_list' or self.context['request'].GET.get('format') == 'html':
            result = instance
        else:
            result = super().to_representation(instance)
        return result

    def create(self, validated_data):
        return Language.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name_pattern = validated_data.get('name_pattern', instance.name_pattern)
        instance.save()

        return instance


class LanguageRelatedField(ModifiedRelatedField):

    def to_representation(self, value):
        data = LanguageSerializer(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return Language.objects.get(pk=data)