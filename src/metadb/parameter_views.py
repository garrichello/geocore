from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .simple_views import SimpleCreateView, SimpleUpdateView, SimpleDeleteView

from .parameter_forms import ParameterForm

from .models import Parameter, ParameterI18N, Language

class ParameterMixin():

    def save_form(self, request, template_name, ctx, create=False):
        ''' Saves the form
        create -- True if creating, False if updating.
        '''
        data = dict()
        form = ctx['forms'][0]
        if form.is_valid():
            obj = form.save()
            obji18n = ParameterI18N()
            obji18n.name = form.cleaned_data['name']
            obji18n.parameter = obj  # Link it with the new Parameter object
            # To save DB consistency we create a new record for all languages.
            # User can update/translate to every other language lately and separately.
            if create:
                for db_lang in Language.objects.all():  # Iterate over all languages in DB
                    obji18n.language = db_lang  # Link it with an existing language
                    obji18n.pk = None  # Clear PK to save data into a new record
                    obji18n.save()  # Save
            else:  # Just update the existing record.
                obji18n.save()

            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)


class ParameterCreateView(ParameterMixin, SimpleCreateView):
    form_class = ParameterForm
    model = Parameter
    template_name = 'metadb/includes/simple_form.html'
    create = True
    ctx = {
        'form_class': 'js-parameter-form',
        'action': reverse_lazy('metadb:parameter_create'),
        'title': _("Create a new meteorological parameter"),
        'submit_name': _("Create parameter"),
        'script': 'metadb/parameter_form.js',
        'attributes': [
            {'name': 'accmodes-url',
             'value': reverse_lazy('metadb:form_load_accmodes')}
        ]
    }
    url_name = 'metadb:parameter_create'


class ParameterUpdateView(ParameterMixin, SimpleUpdateView):
    form_class = ParameterForm
    model = Parameter
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-parameter-form',
        'title': _("Update meteorological parameter"),
        'submit_name': _("Update parameter"),
        'script': 'metadb/parameter_form.js',
        'attributes': [
            {'name': 'accmodes-url',
             'value': reverse_lazy('metadb:form_load_accmodes')}
        ]
    }
    url_name = 'metadb:parameter_update'


class ParameterDeleteView(SimpleDeleteView):
    form_class = ParameterForm
    model = Parameter
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-parameter-delete-form',
        'title': _('Confirm meteorological parameter delete'),
        'text': _('Are you sure you want to delete the parameter'),
        'submit_name': _('Delete parameter')
    }
    url_name = 'metadb:parameter_delete'
