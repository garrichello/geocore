from rest_framework import serializers

from .models import *

class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'label', 'url']
