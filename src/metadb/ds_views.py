from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .forms import DatasetForm

from .models import Dataset

class DatasetBaseView(View):
    form_class = DatasetForm
    model = Dataset

    def save_form(self, request, form, template_name):
        ''' Saves the form '''
        data = dict()
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        ctx = {'form': form}
        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)


class DatasetCreateView(DatasetBaseView):
    template_name = 'metadb/includes/dataset_create_form.html'

    def get(self, request):
        form = self.form_class()

        ctx = {'form': form}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        form = self.form_class(request.POST)
        
        return self.save_form(request, form, self.template_name)


class DatasetUpdateView(DatasetBaseView):
    template_name = 'metadb/includes/dataset_update_form.html'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=obj)

        ctx = {'form': form}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, instance=obj)
        return self.save_form(request, form, self.template_name)


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
