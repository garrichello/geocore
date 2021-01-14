from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import get_language, gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy

from .collection_forms import CollectionForm, CollectionI18NForm

from .models import Collection, Language

class ConveyorBaseView(View):
    form_class = CollectionForm
    formi18n_class = CollectionI18NForm
    model = Collection

    def save_form(self, request, template_name, ctx, create=False):
        ''' Saves the form
        create -- True if creating, False if updating.
        '''
        data = dict()
        col_form = ctx['forms'][0]
        coli18n_form = ctx['forms'][1]
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

        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)

    def get_models(self, pk):
        ''' Just get additional model objects for a given PK '''
        language = get_language()
        col_model = get_object_or_404(self.model, pk=pk)
        coli18n_model = col_model.collectioni18n_set.filter(language__code=language).get()
        orgi18n_model = col_model.organization.organizationi18n_set.filter(language__code=language).get()
        return col_model, coli18n_model, orgi18n_model


class ConveyorCreateView(ConveyorBaseView):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-collection-form',
        'action': reverse_lazy('metadb:collection_create'),
        'title': _("Create a new collection"),
        'submit_name': _("Create collection"),
        'script': 'metadb/collection_form.js',
        'attributes': [
            {'name': 'organizations-url',
             'value': reverse_lazy('metadb:form_load_organizations')}
        ]
    }

    def get(self, request):
        col_form = self.form_class()
        coli18n_form = self.formi18n_class()

        self.ctx['forms'] = [col_form, coli18n_form]
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        col_form = self.form_class(request.POST)
        coli18n_form = self.formi18n_class(request.POST)
        self.ctx['forms'] = [col_form, coli18n_form]
        return self.save_form(request, self.template_name, self.ctx, create=True)


class ConveyorUpdateView(ConveyorBaseView):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-collection-form',           
        'title': _("Update collection"),
        'submit_name': _("Update collection"),
        'script': 'metadb/collection_form.js',
        'attributes': [
            {'name': 'organizations-url', 
             'value': reverse_lazy('metadb:form_load_organizations')}
        ]
    }

    def get(self, request, pk):
        col_model, coli18n_model, orgi18n_model = self.get_models(pk)
        col_form = self.form_class(instance=col_model, orgi18n_pk=orgi18n_model.pk)
        coli18n_form = self.formi18n_class(instance=coli18n_model)

        self.ctx['forms'] = [col_form, coli18n_form]
        self.ctx['action'] = reverse('metadb:collection_update', kwargs={'pk': col_form.instance.pk})
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        col_model_old, coli18n_model_old, _ = self.get_models(pk)
        col_form = self.form_class(request.POST, instance=col_model_old)
        coli18n_form = self.formi18n_class(request.POST, instance=coli18n_model_old)
        self.ctx['forms'] = [col_form, coli18n_form]
        self.ctx['action'] = reverse('metadb:collection_update', kwargs={'pk': col_form.instance.pk})
        return self.save_form(request, self.template_name, self.ctx)

class ConveyorDeleteView(ConveyorBaseView):
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-collection-delete-form',
        'title': _('Confirm collection delete'),
        'text': _('Are you sure you want to delete the collection'),
        'submit_name': _('Delete collection')
    }

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        self.ctx['action'] = reverse('metadb:collection_delete', kwargs={'pk': pk})
        self.ctx['label'] = model_obj.label
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        model_obj.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})      
