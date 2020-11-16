from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from django.utils.translation import get_language, gettext_lazy as _
from django.urls import reverse_lazy

from .models import Language, Collection, CollectionI18N
from .models import Dataset
from .models import Data, Resolution, Scenario
from .forms import CollectionForm, CollectionI18NForm
from .forms import DatasetForm, ScenarioForm, ResolutionForm, DataKindForm, FileTypeForm
from .forms import DataForm, DatasetShortForm, SpecificParameterForm
from bootstrap_modal_forms.generic import BSModalCreateView

class MainView(View):

    def get(self, request):

        collection_headers = [
            ('head_none', 'Id'),
            ('head_select', _('Collection label')),
            ('head_select', _('Collection name')),
            ('head_text', _('Collection description')),
            ('head_select', _('Organization')),
            ('head_text', _('Organization URL')),
            ('head_text', _('Collection URL'))
        ]

        dataset_headers = [
            ('head_none', 'Id'),
            ('head_none', _('Visible')),
            ('head_select', _('Collection label')),
            ('head_select', _('Resolution')),
            ('head_select', _('Scenario')),
            ('head_select', _('Data kind')),
            ('head_select', _('File type')),
            ('head_none', _('Time start')),
            ('head_none', _('Time end')),
            ('head_text', _('Dataset description')),
        ]

        data_headers = [
            ('head_none', 'Id'),
            ('head_none', _('Visible')),
            ('head_select', _('Collection label')),
            ('head_select', _('Resolution')),
            ('head_select', _('Scenario')),
            ('head_select', _('Parameter')),
            ('head_select', _('Time step')),
            ('head_select', _('Variable name')),
            ('head_select', _('Units')),
            ('head_text', _('Levels names')),
            ('head_text', _('Levels group')),
            ('head_none', _('Levels variable')),
            ('head_none', _('Propery label')),
            ('head_none', _('Property value')),
            ('head_text', _('Root directory')),
            ('head_none', _('File name pattern')),
            ('head_none', _('Scale')),
            ('head_none', _('Offset')),
        ]

        ctx = {
            'collection_headers': collection_headers,
            'dataset_headers': dataset_headers,
            'data_headers': data_headers,
        }
        return render(request, 'metadb/main_view.html', context=ctx)

class CollectionBaseView(View):
    form_class = CollectionForm
    formi18n_class = CollectionI18NForm
    model = Collection

    def save_collection_form(self, request, col_form, coli18n_form, template_name, create=False):
        data = dict()
        if col_form.is_valid() and coli18n_form.is_valid():
            # Get collection object, link it with existing organization and save.
            col = col_form.save(commit=False)
            col.organization = col_form.cleaned_data.get('organizationi18n').organization
            col.save()
            coli18n = coli18n_form.save(commit=False)  # Get i18n collection object
            coli18n.collection = col  # Link it with the new collection
            if create:
                for db_lang in Language.objects.all():  # Iterate over all languages in DB
                    coli18n.language = db_lang  # Link it with an existing language
                    coli18n.pk = None  # Clear PK to save data into a new record
                    coli18n.save()  # Save
            else:
                coli18n.save()

            col_form.save_m2m()  # Save form and many-to-many relations
            coli18n_form.save_m2m()  # Save form and many-to-many relations
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        ctx = {'col_form': col_form, 'coli18n_form': coli18n_form}
        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)

    def get_models(self, pk):
        language = get_language()
        col_model = get_object_or_404(self.model, pk=pk)
        coli18n_model = col_model.collectioni18n_set.filter(language__code=language).get()
        orgi18n_model = col_model.organization.organizationi18n_set.filter(language__code=language).get()
        return col_model, coli18n_model, orgi18n_model


class CollectionCreateView(CollectionBaseView):
    template_name = 'metadb/includes/partial_collection_create.html'

    def get(self, request):
        col_form = self.form_class()
        coli18n_form = self.formi18n_class()

        ctx = {'col_form': col_form, 'coli18n_form': coli18n_form}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        col_form = self.form_class(request.POST)
        coli18n_form = self.formi18n_class(request.POST)
        return self.save_collection_form(request, col_form, coli18n_form, self.template_name, create=True)


class CollectionUpdateView(CollectionBaseView):
    template_name = 'metadb/includes/partial_collection_update.html'

    def get(self, request, pk):
        language = get_language()
        col_model, coli18n_model, orgi18n_model = self.get_models(pk)
        col_form = self.form_class(instance=col_model, orgi18n_pk=orgi18n_model.pk)
        coli18n_form = self.formi18n_class(instance=coli18n_model)

        ctx = {'col_form': col_form, 'coli18n_form': coli18n_form}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        col_model_old, coli18n_model_old, _ = self.get_models(pk)
        col_form = self.form_class(request.POST, instance=col_model_old)
        coli18n_form = self.formi18n_class(request.POST, instance=coli18n_model_old)
        return self.save_collection_form(request, col_form, coli18n_form, self.template_name)

class CollectionDeleteView(CollectionBaseView):
    template_name = 'metadb/includes/partial_collection_delete.html'

    def get(self, request, pk):
        col_model = get_object_or_404(self.model, pk=pk)

        ctx = {'collection': col_model}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        col_model = get_object_or_404(self.model, pk=pk)
        col_model.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})      


#======================================================================================================


class DatasetBaseView(View):
    form_class = DatasetForm
    model = Dataset

    def save_form(self, request, form, template_name):
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
    template_name = 'metadb/includes/partial_dataset_create.html'

    def get(self, request):
        form = self.form_class()

        ctx = {'form': form}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        form = self.form_class(request.POST)
        
        return self.save_form(request, form, self.template_name)


class DatasetUpdateView(DatasetBaseView):
    template_name = 'metadb/includes/partial_dataset_update.html'

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
    template_name = 'metadb/includes/partial_dataset_delete.html'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)

        ctx = {'dataset': obj}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        obj.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})


#======================================================================================================
def load_dataset_resolutions(request):
    template_name = 'metadb/hr/dataset_dropdown_list_options.html'
    collection_id = request.GET.get('collectionId')
    resolutions = {}
    if collection_id:
        resolutions = Resolution.objects.filter(id__in=
            [dataset.resolution.id for dataset in Dataset.objects.filter(collection_id=collection_id)])
    ctx = {'data': resolutions}
    return render(request, template_name, ctx)

def load_dataset_scenarios(request):
    template_name = 'metadb/hr/dataset_dropdown_list_options.html'
    collection_id = request.GET.get('collectionId')
    resolution_id = request.GET.get('resolutionId')
    scenarios = {}
    if collection_id and resolution_id:
        scenarios = Scenario.objects.filter(id__in=
            [dataset.scenario.id for dataset in Dataset.objects.filter(
                collection_id=collection_id, resolution_id=resolution_id)])
    ctx = {'data': scenarios}
    return render(request, template_name, ctx)

class DataBaseView(View):
    form_class = DataForm
    ds_form_class = DatasetShortForm
    sp_form_class = SpecificParameterForm

    model = Data

    def save_form(self, request, form, template_name):
        data = dict()
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        ctx = {'form': form}
        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)


class DataCreateView(DataBaseView):
    template_name = 'metadb/includes/partial_data_create.html'

    def get(self, request):
        form = self.form_class()
        ds_form = self.ds_form_class()
        sp_form = self.sp_form_class()

        ctx = {'form': form, 'ds_form': ds_form, 'sp_form': sp_form}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        form = self.form_class(request.POST)
        
        return self.save_form(request, form, self.template_name)


class DataUpdateView(DataBaseView):
    template_name = 'metadb/includes/partial_data_update.html'

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


class DataDeleteView(DataBaseView):
    template_name = 'metadb/includes/partial_data_delete.html'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)

        ctx = {'data': obj}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        obj.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})
