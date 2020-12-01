from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy

from .scenario_forms import ScenarioForm

from .models import Scenario

class ScenarioBaseView(View):
    form_class = ScenarioForm
    model = Scenario

    def save_form(self, request, template_name, ctx):
        ''' Saves the form
        '''
        data = dict()
        form = ctx['forms'][0]
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)


class ScenarioCreateView(ScenarioBaseView):
    template_name = 'metadb/includes/scenario_form.html'
    ctx = {
        'form_class': 'js-scenario-create-form',
        'action': reverse_lazy('metadb:scenario_create'),
        'title': _("Create a new scenario"),
        'submit_name': _("Create scenario"),
    }

    def get(self, request):
        form = self.form_class()

        self.ctx['forms'] = [form]
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        form = self.form_class(request.POST)
        self.ctx['forms'] = [form]
        return self.save_form(request, self.template_name, self.ctx)


class ScenarioUpdateView(ScenarioBaseView):
    template_name = 'metadb/includes/scenario_form.html'
    ctx = {
        'form_class': 'js-scenario-update-form',
        'title': _("Update scenario"),
        'submit_name': _("Update scenario"),
    }

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=model_obj)

        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse('metadb:scenario_create', kwargs={'pk': form.instance.pk})
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, instance=model_obj)
        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse('metadb:scenario_create', kwargs={'pk': form.instance.pk})
        return self.save_form(request, self.template_name, self.ctx)

class ScenarioDeleteView(ScenarioBaseView):
    template_name = 'metadb/includes/scenario_delete_form.html'

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)

        ctx = {'scenario': model_obj}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        model_obj.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})      
