from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy

from .simple_forms import UnitsI18NForm

from .models import Units, UnitsI18N, Language

class UnitBaseView(View):
    form_class = UnitsI18NForm
    model = UnitsI18N

    def save_form(self, request, template_name, ctx, create=False):
        ''' Saves the form
        create -- True if creating, False if updating.
        '''
        data = dict()
        form = ctx['forms'][0]
        if form.is_valid():
            # Create a new Units object and save to DB.
            org = Units()
            org.save()
            orgi18n = form.save(commit=False)  # Get i18n Units object
            orgi18n.units = org  # Link it with the new Units object
            # To save DB consistency we create a new record for all languages.
            # User can update/translate to every other language lately and separately.
            if create:
                for db_lang in Language.objects.all():  # Iterate over all languages in DB
                    orgi18n.language = db_lang  # Link it with an existing language
                    orgi18n.pk = None  # Clear PK to save data into a new record
                    orgi18n.save()  # Save
            else:  # Just update the existing record.
                orgi18n.save()

            form.save_m2m()  # Save form and many-to-many relations
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)


class UnitCreateView(UnitBaseView):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-unit-create-form',
        'action': reverse_lazy('metadb:unit_create'),
        'title': _("Create a new measurement unit"),
        'submit_name': _("Create unit"),
    }

    def get(self, request):
        form = self.form_class()

        self.ctx['forms'] = [form]
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        form = self.form_class(request.POST)
        self.ctx['forms'] = [form]
        return self.save_form(request, self.template_name, self.ctx, create=True)


class UnitUpdateView(UnitBaseView):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-unit-update-form',
        'title': _("Update measurement unit"),
        'submit_name': _("Update units"),
    }

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=model_obj)

        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse('metadb:unit_update', kwargs={'pk': form.instance.pk}),
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, instance=model_obj)

        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse('metadb:unit_update', kwargs={'pk': form.instance.pk}),
        return self.save_form(request, self.template_name, self.ctx)

class UnitDeleteView(UnitBaseView):
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-unit-delete-form',
        'title': _('Confirm measurement unit delete'),
        'text': _('Are you sure you want to delete the unit'),
        'submit_name': _('Delete units')
    }

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        self.ctx['action'] = reverse('metadb:unit_delete', kwargs={'pk': pk})
        self.ctx['label'] = model_obj.name
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        org_model = get_object_or_404(self.model, pk=pk)
        org_model.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})      
