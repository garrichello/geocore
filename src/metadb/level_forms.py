from django.forms import (ModelForm, CharField)
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

from .models import Level

class LevelForm(ModelForm):

    def set_fields(self):
        # Label
        self.fields['label'].label = _('Label')
        # Name
        self.fields['name'] = CharField()
        self.fields['name'].label = _('Name')

        self.order_fields(['label', 'name'])

    def fill_fields(self):

        if self.instance.pk:
            self.fields['name'].initial = self.instance.leveli18n_set.filter(
                language__code=get_language()
            ).get().name

    class Meta:
        model = Level
        fields = ['label']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_fields()

        self.fill_fields()
