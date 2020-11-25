from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from django.forms import (ModelChoiceField, ModelForm, Textarea)

from .models import (Collection, CollectionI18N, OrganizationI18N)


class CollectionForm(ModelForm):
    
    empty_label = '*'

    class Meta:
        model = Collection
        fields = ['label', 'url']
        labels = {
            'label': _('Collection label'),
            'url': _('Collection URL'),
        }

    def __init__(self, *args, **kwargs):
        orgi18n_pk = kwargs.pop('orgi18n_pk', None)
        super(CollectionForm, self).__init__(*args, **kwargs)

        qset = OrganizationI18N.objects.filter(language__code=get_language())
        self.fields['organizationi18n'] = ModelChoiceField(queryset=qset, initial=orgi18n_pk)
        self.fields['organizationi18n'].label = _('Organization')
        self.fields['organizationi18n'].empty_label = self.empty_label


class CollectionI18NForm(ModelForm):

    class Meta:
        model = CollectionI18N
        fields = ['name', 'description']
        labels = {
            'name': _('Collection name'),
            'description': _('Collection description'),
        }
        widgets = {
            'description': Textarea(attrs={'rows': 3}),
        }





