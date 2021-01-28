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
        instance.subpath1 = validated_data.get('subpath1', instance.subpath0)
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
#        self.fields['is_visible'].style = {'template': 'metadb/custom_input.html'}
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
