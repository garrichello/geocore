from django.forms import (ModelForm, CharField, ModelChoiceField, HiddenInput)
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.urls import reverse

from .models import LevelsGroup, UnitsI18N

class LevelsGroupForm(ModelForm):

    def set_fields(self):
        # Description
        self.fields['description'] = CharField()
        self.fields['description'].label = _('Description')
        # Units
        qset = UnitsI18N.objects.filter(language__code=get_language())
        self.fields['unitsi18n'] = ModelChoiceField(queryset=qset)
        self.fields['unitsi18n'].label = _('Measurement unit')
        self.fields['unitsi18n'].empty_label = '*'
        self.fields['unitsi18n'].data_url = reverse('metadb:unit_create')

        self.fields['selected_levels'] = CharField(widget=HiddenInput())
        self.fields['selected_levels'].label = _('Select levels')

        self.order_fields(['description', 'units'])

    def fill_fields(self):

        if self.instance.pk:
            self.fields['unitsi18n'].queryset = UnitsI18N.objects.filter(
                language__code=get_language())
            self.fields['unitsi18n'].initial = self.instance.units.unitsi18n_set.filter(
                language__code=get_language()
            ).get().name

    class Meta:
        model = LevelsGroup
        fields = ['description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_fields()

        self.fill_fields()
