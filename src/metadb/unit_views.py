from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from .common_views import CommonCreateView, CommonUpdateView, CommonDeleteView

from .simple_forms import UnitsI18NForm

from .models import Units, UnitsI18N, Language

class UnitMixin():
    form_class = UnitsI18NForm
    model = UnitsI18N
    create = False

    def save_form(self, request, template_name, ctx):
        ''' Saves the form
        create -- True if creating, False if updating.
        '''
        data = dict()
        form = ctx['forms'][0]
        if form.is_valid():
            # Create a new Units object and save to DB.
            org = Units()
            org.save()
            orgi18n = form.save(commit=False)  # Get i18n Units object
            orgi18n.units = org  # Link it with the new Units object
            # To save DB consistency we create a new record for all languages.
            # User can update/translate to every other language lately and separately.
            if self.create:
                for db_lang in Language.objects.all():  # Iterate over all languages in DB
                    orgi18n.language = db_lang  # Link it with an existing language
                    orgi18n.pk = None  # Clear PK to save data into a new record
                    orgi18n.save()  # Save
            else:  # Just update the existing record.
                orgi18n.save()

            form.save_m2m()  # Save form and many-to-many relations
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)


class UnitCreateView(UnitMixin, CommonCreateView):
    create = True
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-unit-form',
        'title': _("Create a new measurement unit"),
        'submit_name': _("Create unit"),
    }
    action_url = 'metadb:unit_create'


class UnitUpdateView(UnitMixin, CommonUpdateView):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-unit-form',
        'title': _("Update measurement unit"),
        'submit_name': _("Update units"),
    }
    action_url = 'metadb:unit_update'


class UnitDeleteView(CommonDeleteView):
    form_class = UnitsI18NForm
    model = UnitsI18N
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-unit-delete-form',
        'title': _('Confirm measurement unit delete'),
        'text': _('Are you sure you want to delete the unit'),
        'submit_name': _('Delete units')
    }
    action_url = 'metadb:unit_delete'
