from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import get_language
from django.shortcuts import get_object_or_404
from time import sleep

from .collection_forms import CollectionForm, CollectionI18NForm

from .models import Collection, Language, OrganizationI18N


class CollectionBaseView(View):
    form_class = CollectionForm
    formi18n_class = CollectionI18NForm
    model = Collection

    def save_form(self, request, col_form, coli18n_form, template_name, create=False):
        ''' Saves the form
        create -- True if creating, False if updating.
        '''
        data = dict()
        if col_form.is_valid() and coli18n_form.is_valid():
            # Get collection object, link it with existing organization and save.
            col = col_form.save(commit=False)
            col.organization = col_form.cleaned_data.get('organizationi18n').organization
            col.save()
            coli18n = coli18n_form.save(commit=False)  # Get i18n collection object
            coli18n.collection = col  # Link it with the new collection
            # To save DB consistency we create a new record for all languages.
            # User can update/translate to every other language lately and separately.
            if create:
                for db_lang in Language.objects.all():  # Iterate over all languages in DB
                    coli18n.language = db_lang  # Link it with an existing language
                    coli18n.pk = None  # Clear PK to save data into a new record
                    coli18n.save()  # Save
            else:  # Just update the existing record.
                coli18n.save()

            col_form.save_m2m()  # Save form and many-to-many relations
            coli18n_form.save_m2m()  # Save form and many-to-many relations
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        ctx = {'forms': [col_form, coli18n_form], 'pk': col_form.instance.pk}
        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)

    def get_models(self, pk):
        ''' Just get additional model objects for a given PK '''
        language = get_language()
        col_model = get_object_or_404(self.model, pk=pk)
        coli18n_model = col_model.collectioni18n_set.filter(language__code=language).get()
        orgi18n_model = col_model.organization.organizationi18n_set.filter(language__code=language).get()
        return col_model, coli18n_model, orgi18n_model


class CollectionCreateView(CollectionBaseView):
    template_name = 'metadb/includes/collection_create_form.html'

    def get(self, request):
        col_form = self.form_class()
        coli18n_form = self.formi18n_class()

        ctx = {'forms': [col_form, coli18n_form], 'form_class': 'js-collection-create-form'}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        col_form = self.form_class(request.POST)
        coli18n_form = self.formi18n_class(request.POST)
        return self.save_form(request, col_form, coli18n_form, self.template_name, create=True)


class CollectionUpdateView(CollectionBaseView):
    template_name = 'metadb/includes/collection_update_form.html'

    def get(self, request, pk):
        language = get_language()
        col_model, coli18n_model, orgi18n_model = self.get_models(pk)
        col_form = self.form_class(instance=col_model, orgi18n_pk=orgi18n_model.pk)
        coli18n_form = self.formi18n_class(instance=coli18n_model)

        ctx = {'forms': [col_form, coli18n_form], 
               'form_class': 'js-collection-update-form', 'pk': col_form.instance.pk}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        col_model_old, coli18n_model_old, _ = self.get_models(pk)
        col_form = self.form_class(request.POST, instance=col_model_old)
        coli18n_form = self.formi18n_class(request.POST, instance=coli18n_model_old)
        return self.save_form(request, col_form, coli18n_form, self.template_name)

class CollectionDeleteView(CollectionBaseView):
    template_name = 'metadb/includes/collection_delete_form.html'

    def get(self, request, pk):
        col_model = get_object_or_404(self.model, pk=pk)

        ctx = {'collection': col_model}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        col_model = get_object_or_404(self.model, pk=pk)
        col_model.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})      
