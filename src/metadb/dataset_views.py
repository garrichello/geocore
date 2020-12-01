from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy

from .dataset_forms import DatasetForm

from .models import Dataset


class DatasetBaseView(View):
    form_class = DatasetForm
    model = Dataset

    def save_form(self, request, template_name, ctx):
        ''' Saves the form '''
        data = dict()
        form = ctx['forms'][0]
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)


class DatasetCreateView(DatasetBaseView):
    template_name = 'metadb/includes/dataset_form.html'
    ctx = {
        'form_class': 'js-dataset-create-form',
        'action': reverse_lazy('metadb:dataset_create'),
        'title': _("Create a new dataset"),
        'submit_name': _("Create dataset"),
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


class DatasetUpdateView(DatasetBaseView):
    template_name = 'metadb/includes/dataset_form.html'
    ctx = {
        'form_class': 'js-dataset-update-form',
        'title': _("Update dataset"),
        'submit_name': _("Update dataset"),
    }

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=obj)

        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse('metadb:dataset_update', kwargs={'pk': form.instance.pk})
        html_form = render_to_string(self.template_name, request, self.ctx)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, instance=obj)
        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse('metadb:dataset_update', kwargs={'pk': form.instance.pk})
        return self.save_form(request, self.template_name, self.ctx)


class DatasetDeleteView(DatasetBaseView):
    template_name = 'metadb/includes/dataset_delete_form.html'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)

        ctx = {'dataset': obj}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        obj.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})
