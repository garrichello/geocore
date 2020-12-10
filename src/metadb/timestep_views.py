from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .simple_views import CommonCreateView, CommonUpdateView, CommonDeleteView

from .timestep_forms import TimeStepForm

from .models import TimeStep, TimeStepI18N, Language

class TimeStepMixin():

    def save_form(self, request, template_name, ctx, create=False):
        ''' Saves the form
        create -- True if creating, False if updating.
        '''
        data = dict()
        form = ctx['forms'][0]
        if form.is_valid():
            obj = form.save()
            obji18n = TimeStepI18N()
            obji18n.name = form.cleaned_data['name']
            obji18n.time_step = obj  # Link it with the new TimeStep object
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


class TimeStepCreateView(TimeStepMixin, CommonCreateView):
    form_class = TimeStepForm
    model = TimeStep
    template_name = 'metadb/includes/simple_form.html'
    create = True
    ctx = {
        'form_class': 'js-timestep-form',
        'action': reverse_lazy('metadb:timestep_create'),
        'title': _("Create a new time step"),
        'submit_name': _("Create time step"),
    }
    url_name = 'metadb:time_step_create'


class TimeStepUpdateView(TimeStepMixin, CommonUpdateView):
    form_class = TimeStepForm
    model = TimeStep
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-timestep-form',
        'title': _("Update time step"),
        'submit_name': _("Update time step"),
    }
    url_name = 'metadb:time_step_update'


class TimeStepDeleteView(CommonDeleteView):
    form_class = TimeStepForm
    model = TimeStep
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-timestep-delete-form',
        'title': _('Confirm time step delete'),
        'text': _('Are you sure you want to delete the time step'),
        'submit_name': _('Delete time step')
    }
    url_name = 'metadb:time_step_delete'
