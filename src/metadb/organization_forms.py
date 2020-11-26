from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm

from .models import (Organization, OrganizationI18N)


class OrganizationForm(ModelForm):

    class Meta:
        model = Organization
        fields = ['url']
        labels = {
            'url': _('Organization URL'),
        }

class OrganizationI18NForm(ModelForm):

    class Meta:
        model = OrganizationI18N
        fields = ['name']
        labels = {
            'name': _('Organization name'),
        }
