from django.forms import ModelForm, CharField
from django.utils.translation import get_language, gettext_lazy as _

from .models import Units


class UnitsForm(ModelForm):

    class Meta:
        model = Units
        fields = ['id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'] = CharField()
        self.fields['name'].label = _('Measurement unit name')

        if self.instance.pk:
            self.fields['name'].initial = self.instance.unitsi18n_set.filter(
                language__code=get_language()).get().name
