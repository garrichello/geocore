from django.forms import (ModelForm, Textarea)
from django.shortcuts import reverse

from .models import Dataset, Collection, Resolution, Scenario, DataKind, FileType


class DatasetForm(ModelForm):

    empty_label = '*'

    class Meta:
        model = Dataset
        fields = '__all__'

        widgets = {
            'description': Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.keys():
            self.fields[field].empty_label = self.empty_label

        self.fields['collection'].queryset = Collection.objects.order_by('label')
        self.fields['collection'].data_url = reverse('metadb:collection_create')
        self.fields['resolution'].queryset = Resolution.objects.order_by('name')
        self.fields['resolution'].data_url = reverse('metadb:resolution_create')
        self.fields['scenario'].queryset = Scenario.objects.order_by('name')
#        self.fields['scenario'].data_url = reverse('metadb:scenario_create')
        self.fields['data_kind'].queryset = DataKind.objects.order_by('name')
#        self.fields['data_kind'].data_url = reverse('metadb:datakind_create')
        self.fields['file_type'].queryset = FileType.objects.order_by('name')
#        self.fields['file_type'].data_url = reverse('metadb:filetype_create')
