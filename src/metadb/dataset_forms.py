from django.forms import (ModelForm, Textarea)

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
