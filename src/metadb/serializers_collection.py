from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.renderers import *
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

from .models import *
from .serializers import ModifiedRelatedField


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
    serializer = OrganizationSerializer
    model = Organization


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
    serializer = CollectionSerializer
    model = Collection
#    data_field = 'label'
