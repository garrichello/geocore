from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import get_language, gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy

from .simple_forms import OrganizationForm, OrganizationI18NForm

from .models import Organization, Language

class OrganizationBaseView(View):
    form_class = OrganizationForm
    formi18n_class = OrganizationI18NForm
    model = Organization

    def save_form(self, request, template_name, ctx, create=False):
        ''' Saves the form
        create -- True if creating, False if updating.
        '''
        data = dict()
        orgi18n_form = ctx['forms'][0]
        org_form = ctx['forms'][1]
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

        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)

    def get_models(self, pk):
        ''' Just get additional model objects for a given PK '''
        model_obj = get_object_or_404(self.model, pk=pk)
        modeli18n_obj = model_obj.organizationi18n_set.filter(language__code=get_language()).get()
        return model_obj, modeli18n_obj


class OrganizationCreateView(OrganizationBaseView):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-organization-create-form',
        'action': reverse_lazy('metadb:organization_create'),
        'title': _("Create a new organization"),
        'submit_name': _("Create organization"),
    }

    def get(self, request):
        org_form = self.form_class()
        orgi18n_form = self.formi18n_class()

        self.ctx['forms'] = [orgi18n_form, org_form]
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        org_form = self.form_class(request.POST)
        orgi18n_form = self.formi18n_class(request.POST)
        self.ctx['forms'] = [orgi18n_form, org_form]
        return self.save_form(request, self.template_name, self.ctx, create=True)


class OrganizationUpdateView(OrganizationBaseView):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-organization-update-form',
        'title': _("Update organization"),
        'submit_name': _("Update organization"),
    }

    def get(self, request, pk):
        org_model, orgi18n_model = self.get_models(pk)
        org_form = self.form_class(instance=org_model)
        orgi18n_form = self.formi18n_class(instance=orgi18n_model)

        self.ctx['forms'] = [orgi18n_form, org_form]
        self.ctx['action'] = reverse('metadb:organization_update', kwargs={'pk': org_form.instance.pk}),
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        org_model_old, orgi18n_model_old = self.get_models(pk)
        org_form = self.form_class(request.POST, instance=org_model_old)
        orgi18n_form = self.formi18n_class(request.POST, instance=orgi18n_model_old)
        self.ctx['forms'] = [orgi18n_form, org_form]
        self.ctx['action'] = reverse('metadb:organization_update', kwargs={'pk': org_form.instance.pk}),
        return self.save_form(request, self.template_name, self.ctx)

class OrganizationDeleteView(OrganizationBaseView):
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-organization-delete-form',
        'title': _('Confirm organization delete'),
        'text': _('Are you sure you want to delete the organization'),
        'submit_name': _('Delete organization')
    }

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        self.ctx['action'] = reverse('metadb:organization_delete', kwargs={'pk': pk})
        self.ctx['label'] = model_obj.label
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        org_model = get_object_or_404(self.model, pk=pk)
        org_model.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})      
