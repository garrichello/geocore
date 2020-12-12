from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .common_views import CommonCreateView, CommonUpdateView, CommonDeleteView

from .level_forms import LevelForm

from .models import Level, LevelI18N, Language

class LevelMixin():
    form_class = LevelForm
    model = Level
    create = False  # True for Create, False - for Update. Overriden in Create class.

    def save_form(self, request, template_name, ctx):
        ''' Saves the form
        create -- True if creating, False if updating.
        '''
        data = dict()
        form = ctx['forms'][0]
        if form.is_valid():
            obj = form.save()
            obji18n = LevelI18N()
            obji18n.name = form.cleaned_data['name']
            obji18n.level = obj  # Link it with the new Level object
            # To save DB consistency we create a new record for all languages.
            # User can update/translate to every other language lately and separately.
            if self.create:
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


class LevelCreateView(LevelMixin, CommonCreateView):
    template_name = 'metadb/includes/simple_form.html'
    create = True

    ctx = {
        'form_class': 'js-level-form',
        'action': reverse_lazy('metadb:level_create'),
        'title': _("Create a new level"),
        'submit_name': _("Create level"),
    }
    action_url = 'metadb:level_create'


class LevelUpdateView(LevelMixin, CommonUpdateView):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-level-form',
        'title': _("Update level"),
        'submit_name': _("Update level"),
    }
    action_url = 'metadb:level_update'


class LevelDeleteView(CommonDeleteView):
    form_class = LevelForm
    model = Level
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-level-delete-form',
        'title': _('Confirm level delete'),
        'text': _('Are you sure you want to delete the level'),
        'submit_name': _('Delete level')
    }
    action_url = 'metadb:level_delete'
