from collections import OrderedDict

from rest_framework import serializers
from rest_framework.renderers import *
from django.utils.translation import gettext_lazy as _

from .models import *


class ModifiedRelatedField(serializers.RelatedField):
    serializer = lambda value, context: None
    model = None
    data_field = None
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

    def get_serializer(self):
        return self.serializer

    def get_model(self):
        return self.model

    def to_representation(self, value):
        data = self.get_serializer()(value, context=self.context).data
        action = self.context['request'].META.get('HTTP_ACTION')
        result = data[self.data_field] if self.data_field else data
        if action == 'update':
            result = result.get('id', None)
        return result

    def to_internal_value(self, data):
        return self.get_model().objects.get(pk=data)


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
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.save()
        return instance


class LanguageRelatedField(ModifiedRelatedField):
    serializer = LanguageSerializer
    model = Language
