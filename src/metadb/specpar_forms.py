from django.utils.translation import get_language
from django.forms import (ModelForm, ModelChoiceField, Textarea, CharField)
from django.utils.translation import gettext_lazy as _

from .models import (SpecificParameter, ParameterI18N, TimeStepI18N, LevelsGroup,
                     Parameter, TimeStep)


class SpecificParameterForm(ModelForm):

    empty_label = '*'

    def set_fields(self):
        language = get_language()
        # Parameter
        qset = ParameterI18N.objects.filter(language__code=language).order_by('name')
        self.fields['parameteri18n'] = ModelChoiceField(queryset=qset)
        self.fields['parameteri18n'].empty_label = self.empty_label
        self.fields['parameteri18n'].label = _('Parameter')
        # Time step
        qset = TimeStepI18N.objects.filter(language__code=language).order_by('name')
        self.fields['time_stepi18n'] = ModelChoiceField(queryset=qset)
        self.fields['time_stepi18n'].empty_label = self.empty_label
        self.fields['time_stepi18n'].label = _('Time step')
        # Levels group
        self.fields['levels_group'].empty_label = self.empty_label
        self.fields['levels_group'].label = _('Levels group')
        # Levels names
        self.fields['levels_namesi18n'] = CharField(widget=Textarea(attrs={'rows': 3}), disabled=True)
        self.fields['levels_namesi18n'].label = _('Levels names')
        self.fields['levels_namesi18n'].required = False

        self.order_fields(['parameteri18n', 'time_stepi18n', 'levels_group', 'levels_namesi18n'])


    class Meta:
        model = SpecificParameter
        fields = ['levels_group']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_fields()
