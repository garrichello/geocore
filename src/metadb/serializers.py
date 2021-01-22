from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.shortcuts import reverse

from .models import *


class OrganizationI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationI18N
        fields = ['id', 'name']

    def to_representation(self, data):
        data = data.filter(language__code=get_language()).get()
        return super().to_representation(data)


class OrganizationSerializer(serializers.ModelSerializer):
    organizationi18n = OrganizationI18NSerializer(source='organizationi18n_set')
    class Meta:
        model = Organization
        fields = ['id', 'url', 'organizationi18n']


class CollectionI18NSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollectionI18N
        fields = ['id', 'name', 'description']

    def to_representation(self, data):
        data = data.filter(language__code=get_language()).get()
        return super().to_representation(data)


class CollectionSerializer(serializers.ModelSerializer):
    collectioni18n = CollectionI18NSerializer(source='collectioni18n_set')
    organization = OrganizationSerializer()
    class Meta:
        model = Collection
        fields = ['id', 'label', 'url', 'collectioni18n', 'organization']

    def create(self, validated_data):
        print(validated_data)
        return None

