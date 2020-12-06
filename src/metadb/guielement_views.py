from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import get_language, gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy

from .simple_forms import GuiElementForm, GuiElementI18NForm

from .models import GuiElement, Language

class GuiElementBaseView(View):
    form_class = GuiElementForm
    formi18n_class = GuiElementI18NForm
    model = GuiElement

    def save_form(self, request, template_name, ctx, create=False):
        ''' Saves the form
        create -- True if creating, False if updating.
        '''
        data = dict()
        gui_form = ctx['forms'][0]
        guii18n_form = ctx['forms'][1]
        if gui_form.is_valid() and guii18n_form.is_valid():
            # Get GUI element object save.
            gui = gui_form.save()
            guii18n = guii18n_form.save(commit=False)  # Get i18n GUI element object
            guii18n.gui_element = gui  # Link it with the new GUI element
            # To save DB consistency we create a new record for all languages.
            # User can update/translate to every other language lately and separately.
            if create:
                for db_lang in Language.objects.all():  # Iterate over all languages in DB
                    guii18n.language = db_lang  # Link it with an existing language
                    guii18n.pk = None  # Clear PK to save data into a new record
                    guii18n.save()  # Save
            else:  # Just update the existing record.
                guii18n.save()

            guii18n_form.save_m2m()  # Save form and many-to-many relations
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)

    def get_models(self, pk):
        ''' Just get additional model objects for a given PK '''
        model_obj = get_object_or_404(self.model, pk=pk)
        modeli18n_obj = model_obj.guielementi18n_set.filter(language__code=get_language()).get()
        return model_obj, modeli18n_obj


class GuiElementCreateView(GuiElementBaseView):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-gui-element-form',
        'action': reverse_lazy('metadb:gui_element_create'),
        'title': _("Create a new GUI element"),
        'submit_name': _("Create GUI element"),
    }

    def get(self, request):
        gui_form = self.form_class()
        guii18n_form = self.formi18n_class()

        self.ctx['forms'] = [gui_form, guii18n_form]
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        gui_form = self.form_class(request.POST)
        guii18n_form = self.formi18n_class(request.POST)
        self.ctx['forms'] = [gui_form, guii18n_form]
        return self.save_form(request, self.template_name, self.ctx, create=True)


class GuiElementUpdateView(GuiElementBaseView):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-gui-element-form',
        'title': _("Update GUI element"),
        'submit_name': _("Update GUI element"),
    }

    def get(self, request, pk):
        gui_model, guii18n_model = self.get_models(pk)
        gui_form = self.form_class(instance=gui_model)
        guii18n_form = self.formi18n_class(instance=guii18n_model)

        self.ctx['forms'] = [gui_form, guii18n_form]
        self.ctx['action'] = reverse('metadb:gui_element_update', kwargs={'pk': gui_form.instance.pk}),
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        gui_model_old, guii18n_model_old = self.get_models(pk)
        gui_form = self.form_class(request.POST, instance=gui_model_old)
        guii18n_form = self.formi18n_class(request.POST, instance=guii18n_model_old)
        self.ctx['forms'] = [gui_form, guii18n_form]
        self.ctx['action'] = reverse('metadb:gui_element_update', kwargs={'pk': gui_form.instance.pk}),
        return self.save_form(request, self.template_name, self.ctx)

class GuiElementDeleteView(GuiElementBaseView):
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-gui-element-delete-form',
        'title': _('Confirm GUI element delete'),
        'text': _('Are you sure you want to delete the GUI element'),
        'submit_name': _('Delete GUI element')
    }

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        self.ctx['action'] = reverse('metadb:gui_element_delete', kwargs={'pk': pk})
        self.ctx['label'] = model_obj.label
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        gui_model = get_object_or_404(self.model, pk=pk)
        gui_model.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})      
