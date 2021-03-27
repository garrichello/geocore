from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.renderers import *
from django.utils.translation import gettext_lazy as _

from .serializers_collection import CollectionRelatedField

from .models import *
from .serializers import ModifiedRelatedField


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
    serializer = ScenarioSerializer
    model = Scenario


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
    serializer = ResolutionSerializer
    model = Resolution


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
    serializer = DataKindSerializer
    model = DataKind
    data_field = 'name'


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
    serializer = FileTypeSerializer
    model = FileType
    data_field = 'name'


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
    serializer = DatasetSerializer
    model = Dataset
