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


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    organizationi18n = OrganizationI18NSerializer(source='organizationi18n_set')
    dataurl = serializers.HyperlinkedIdentityField(view_name='metadb:organization-detail',
                                                   read_only=True)    
    class Meta:
        model = Organization
        fields = ['id', 'dataurl', 'url', 'organizationi18n']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['url'].label = _('Organization URL')


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
    qset = Organization.objects.all()
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
