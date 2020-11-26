from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from time import sleep

from .dataset_forms import DatasetForm

from .models import Dataset, Collection, Resolution, Scenario, DataKind, FileType

def load_collections(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    collections = Collection.objects.order_by('label').all()
    ctx = {'data': collections}
    return render(request, template_name, ctx)


def load_resolutions(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    resolutions = Resolution.objects.order_by('name').all()
    ctx = {'data': resolutions}
    return render(request, template_name, ctx)


def load_scenarios(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    scenarios = Scenario.objects.order_by('name').all()
    ctx = {'data': scenarios}
    return render(request, template_name, ctx)


def load_datakinds(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    datakinds = DataKind.objects.order_by('name').all()
    ctx = {'data': datakinds}
    return render(request, template_name, ctx)


def load_filetypes(request):
    template_name = 'metadb/hr/dropdown_list_options.html'
    sleep(0.1)  # Have to wait for DB to arrange things.
    filetypes = FileType.objects.order_by('name').all()
    ctx = {'data': filetypes}
    return render(request, template_name, ctx)


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

        ctx = {'forms': [form]}
        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)


class DatasetCreateView(DatasetBaseView):
    template_name = 'metadb/includes/dataset_create_form.html'

    def get(self, request):
        form = self.form_class()

        ctx = {'forms': [form]}
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

        ctx = {'forms': [form], 'pk': form.instance.pk}
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
