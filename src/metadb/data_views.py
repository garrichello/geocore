from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .data_forms import DataForm

from .models import (Data, Dataset, SpecificParameter)


class DataBaseView(View):
    form_class = DataForm
    model = Data

    def save_form(self, request, form, template_name):
        ''' Saves the form '''
        data = dict()
        if form.is_valid():
            data_obj = form.save(commit=False)  # Get data object
            # Find and attach dataset object to the data object
            dataset_obj = Dataset.objects.filter(
                collection=form.cleaned_data['collection'],
                resolution=form.cleaned_data['resolution'],
                scenario=form.cleaned_data['scenario']
            ).get()
            data_obj.dataset = dataset_obj
            # Find and attach specific parameter object to the data object
            sp_obj = SpecificParameter.objects.filter(
                parameter=form.cleaned_data['parameteri18n'].parameter,
                time_step=form.cleaned_data['time_stepi18n'].time_step,
                levels_group=form.cleaned_data['levels_group']
            ).get()
            data_obj.specific_parameter = sp_obj
            # Get and sttach units object to the data object
            data_obj.units = form.cleaned_data['unitsi18n'].units

            data_obj.save()  # Save object
            form.save_m2m()  # Save many-to-many relations
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        ctx = {'forms': [form]}
        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)


class DataCreateView(DataBaseView):
    template_name = 'metadb/includes/data_create_form.html'

    def get(self, request):
        form = self.form_class()

        ctx = {'forms': [form], 'form_class': 'js-data-create-form'}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        form = self.form_class(request.POST)
        
        return self.save_form(request, form, self.template_name)


class DataUpdateView(DataBaseView):
    template_name = 'metadb/includes/data_update_form.html'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=obj)

        ctx = {'forms': [form], 'form_class': 'js-data-update-form', 'pk': form.instance.pk}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, instance=obj)
        return self.save_form(request, form, self.template_name)


class DataDeleteView(DataBaseView):
    template_name = 'metadb/includes/data_delete_form.html'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)

        ctx = {'data': obj}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        obj.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})
