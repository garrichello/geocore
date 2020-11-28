from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import get_language
from django.shortcuts import get_object_or_404

from .organization_forms import OrganizationForm, OrganizationI18NForm

from .models import Organization, Language

class OrganizationBaseView(View):
    form_class = OrganizationForm
    formi18n_class = OrganizationI18NForm
    model = Organization

    def save_form(self, request, org_form, orgi18n_form, template_name, create=False):
        ''' Saves the form
        create -- True if creating, False if updating.
        '''
        data = dict()
        if org_form.is_valid() and orgi18n_form.is_valid():
            # Get organization object save.
            org = org_form.save()
            orgi18n = orgi18n_form.save(commit=False)  # Get i18n organization object
            orgi18n.organization = org  # Link it with the new organization
            # To save DB consistency we create a new record for all languages.
            # User can update/translate to every other language lately and separately.
            if create:
                for db_lang in Language.objects.all():  # Iterate over all languages in DB
                    orgi18n.language = db_lang  # Link it with an existing language
                    orgi18n.pk = None  # Clear PK to save data into a new record
                    orgi18n.save()  # Save
            else:  # Just update the existing record.
                orgi18n.save()

            orgi18n_form.save_m2m()  # Save form and many-to-many relations
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        ctx = {'forms': [orgi18n_form, org_form], 'pk': org_form.instance.pk}
        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)

    def get_models(self, pk):
        ''' Just get additional model objects for a given PK '''
        language = get_language()
        model_obj = get_object_or_404(self.model, pk=pk)
        modeli18n_obj = model_obj.organizationi18n_set.filter(language__code=language).get()
        return model_obj, modeli18n_obj


class OrganizationCreateView(OrganizationBaseView):
    template_name = 'metadb/includes/organization_create_form.html'

    def get(self, request):
        org_form = self.form_class()
        orgi18n_form = self.formi18n_class()

        ctx = {'forms': [orgi18n_form, org_form]}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        org_form = self.form_class(request.POST)
        orgi18n_form = self.formi18n_class(request.POST)
        return self.save_form(request, org_form, orgi18n_form, self.template_name, create=True)


class OrganizationUpdateView(OrganizationBaseView):
    template_name = 'metadb/includes/organization_update_form.html'

    def get(self, request, pk):
        language = get_language()
        org_model, orgi18n_model = self.get_models(pk)
        org_form = self.form_class(instance=org_model)
        orgi18n_form = self.formi18n_class(instance=orgi18n_model)

        ctx = {'forms': [orgi18n_form, org_form], 'pk': org_form.instance.pk}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        org_model_old, orgi18n_model_old = self.get_models(pk)
        org_form = self.form_class(request.POST, instance=org_model_old)
        orgi18n_form = self.formi18n_class(request.POST, instance=orgi18n_model_old)
        return self.save_form(request, org_form, orgi18n_form, self.template_name)

class OrganizationDeleteView(OrganizationBaseView):
    template_name = 'metadb/includes/organization_delete_form.html'

    def get(self, request, pk):
        org_model = get_object_or_404(self.model, pk=pk)

        ctx = {'organization': org_model}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        org_model = get_object_or_404(self.model, pk=pk)
        org_model.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})      
