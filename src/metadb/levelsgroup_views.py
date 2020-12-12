from .common_views import CommonCreateView, CommonUpdateView, CommonDeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string

from .levelsgroup_form import LevelsGroupForm

from .models import LevelsGroup, Level

import json

class LevelsGroupMixin():
    form_class = LevelsGroupForm
    model = LevelsGroup

    def save_form(self, request, template_name, ctx):
        ''' Saves the form '''
        data = dict()
        form = ctx['forms'][0]
        if form.is_valid():
            obj = form.save(commit=False)
            obj.units = form.cleaned_data['unitsi18n'].units
            lvs_names = json.loads(form.cleaned_data['selected_levels'])
            lvs_objs = Level.objects.filter(label__in=lvs_names)
            obj.save()
            obj.level.set(lvs_objs)
            form.save_m2m()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)


class LevelsGroupCreateView(LevelsGroupMixin, CommonCreateView):
    template_name = 'metadb/includes/levelsgroup_form.html'
    ctx = {
        'form_class': 'js-levels-group-form',
        'title': _("Create a new levels group"),
        'submit_name': _("Create levels group"),
        'script': 'metadb/levelsgroup_form.js',
        'attributes': [
            {'name': 'units-url',
             'value': reverse_lazy('metadb:form_load_units')},
            {'name': 'levels-url',
             'value': reverse_lazy('metadb:form_load_levels')},
        ]
    }
    action_url = 'metadb:levels_group_create'


class LevelsGroupUpdateView(LevelsGroupMixin, CommonUpdateView):
    template_name = 'metadb/includes/levelsgroup_form.html'
    ctx = {
        'form_class': 'js-levels-group-form',
        'title': _("Update levels_group"),
        'submit_name': _("Update levels group"),
        'script': 'metadb/levelsgroup_form.js',
        'attributes': [
            {'name': 'units-url',
             'value': reverse_lazy('metadb:form_load_units')},
            {'name': 'levels-url',
             'value': reverse_lazy('metadb:form_load_levels')},
        ]
    }
    action_url = 'metadb:levels_group_update'

class LevelsGroupDeleteView(CommonDeleteView):
    form_class = LevelsGroupForm
    model = LevelsGroup
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-levels-group-delete-form',
        'title': _('Confirm levels group delete'),
        'text': _('Are you sure you want to delete the levels group'),
        'submit_name': _('Delete levels group')
    }
    action_url = 'metadb:levels_group_delete'
