from django.forms import (ModelForm, Textarea, CharField)
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from .models import Dataset, Collection, Resolution, Scenario, DataKind, FileType


class DatasetForm(ModelForm):

    empty_label = '*'

    def set_fields(self):
        # Collection label
        self.fields['collection'].queryset = Collection.objects.order_by('label')
        self.fields['collection'].data_url = reverse('metadb:collection_create')
        self.fields['collection'].empty_label = self.empty_label
        self.fields['collection'].label = _('Collection label')
        # Horizontal resolution
        self.fields['resolution'].queryset = Resolution.objects.order_by('name')
        self.fields['resolution'].data_url = reverse('metadb:resolution_create')
        self.fields['resolution'].empty_label = self.empty_label
        self.fields['resolution'].label = _('Horizontal resolution')
        # Scenario
        self.fields['scenario'].queryset = Scenario.objects.order_by('name')
        self.fields['scenario'].data_url = reverse('metadb:scenario_create')
        self.fields['scenario'].empty_label = self.empty_label
        self.fields['scenario'].label = _('Scenario')
        # Data kind
        self.fields['data_kind'].queryset = DataKind.objects.order_by('name')
        self.fields['data_kind'].data_url = reverse('metadb:datakind_create')
        self.fields['data_kind'].empty_label = self.empty_label
        self.fields['data_kind'].label = _('Data kind')
        # Description
        self.fields['description'] = CharField(widget=Textarea(attrs={'rows': 3}))
        self.fields['description'].label = _('Description')
        # Is visible
        self.fields['is_visible'].label = _('Visible')
        # Time start
        self.fields['time_start'].label = _('Start date')
        # Time end
        self.fields['time_end'].label = _('End date')
        # File type
        self.fields['file_type'].queryset = FileType.objects.order_by('name')
        self.fields['file_type'].data_url = reverse('metadb:filetype_create')
        self.fields['file_type'].empty_label = self.empty_label
        self.fields['file_type'].label = _('File type')

        self.order_fields(['is_visible', 'collection', 'resolution', 'scenario', 'data_kind',
                          'description', 'time_start', 'time_end', 'file_type'])
    class Meta:
        model = Dataset
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_fields()
