from django.forms import (ModelForm, BooleanField, CharField)
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

from .models import Parameter

class ParameterForm(ModelForm):

    def set_fields(self):
        # Visible
        self.fields['is_visible'] = BooleanField()
        self.fields['is_visible'].initial = True
        self.fields['is_visible'].label = _('Visible')
        # Name
        self.fields['name'] = CharField()
        self.fields['name'].label = _('Parameter')
        # Accumulation mode
        self.fields['accumulation_mode'].empty_label = '*'
        self.fields['accumulation_mode'].label = _('Accumulation mode')

        self.order_fields(['is_visible', 'name', 'accumulation_mode'])

    def fill_fields(self):

        if self.instance.pk:
            self.fields['name'].initial = self.instance.parameteri18n_set.filter(
                language__code=get_language()
            ).get().name

    class Meta:
        model = Parameter
        fields = ['is_visible', 'accumulation_mode']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_fields()

        self.fill_fields()
