from django.forms import (ModelForm, Textarea)
from django.shortcuts import reverse

from .models import Dataset


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

        self.fields['collection'].data_url = reverse('metadb:collection_create')
#        self.fields['resolution'].data_url = reverse('metadb:resolution_create')
#        self.fields['scenario'].data_url = reverse('metadb:scenario_create')
#        self.fields['data_kind'].data_url = reverse('metadb:datakind_create')
#        self.fields['file_type'].data_url = reverse('metadb:filetype_create')
