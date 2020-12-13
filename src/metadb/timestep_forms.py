from django.forms import (ModelForm, CharField)
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

from .models import TimeStep

class TimeStepForm(ModelForm):

    def set_fields(self):
        # Label
        self.fields['label'].label = _('Label')
        # Name
        self.fields['name'] = CharField()
        self.fields['name'].label = _('Name')
        # Subpath
        self.fields['subpath2'].label = _('Time step subpath')

        self.order_fields(['label', 'name', 'subpath2'])

    def fill_fields(self):

        if self.instance.pk:
            self.fields['name'].initial = self.instance.timestepi18n_set.filter(
                language__code=get_language()
            ).get().name

    class Meta:
        model = TimeStep
        fields = ['label', 'subpath2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_fields()

        self.fill_fields()
