from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import get_language
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .models import Language

class Common2Mixin():
    form_class = None
    formi18n_class = None
    model = None
    create = False

    def save_valid_forms(self, form, formi18n, fk_field_name):
        obj = form.save()
        obji18n = formi18n.save(commit=False)  # Get i18n element object
        setattr(obji18n, fk_field_name, obj)  # Link it with the new GUI element
        # To save DB consistency we create a new record for all languages.
        # User can update/translate to every other language lately and separately.
        if self.create:
            for db_lang in Language.objects.all():  # Iterate over all languages in DB
                obji18n.language = db_lang  # Link it with an existing language
                obji18n.pk = None  # Clear PK to save data into a new record
                obji18n.save()  # Save
        else:  # Just update the existing record.
            obji18n.save()
        formi18n.save_m2m()  # Save form and many-to-many relations

    def save_form(self, request, template_name, ctx, fk_field_name):
        ''' Saves the form
        '''
        data = dict()
        form = ctx['forms'][0]
        formi18n = ctx['forms'][1]
        if form.is_valid() and formi18n.is_valid():
            self.save_valid_forms(form, formi18n, fk_field_name)
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)

    def get_models(self, pk, reverse_field_name):
        ''' Just get additional model objects for a given PK '''
        model_obj = get_object_or_404(self.model, pk=pk)
        modeli18n_obj = getattr(model_obj, reverse_field_name+'_set').filter(language__code=get_language()).get()
        return model_obj, modeli18n_obj


class Common2CreateView(Common2Mixin, View):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': '',
        'title': '',
        'submit_name': '',
    }
    action_url = ''
    fk_field_name = ''
    create = True

    def get(self, request):
        form = self.form_class()  # pylint: disable=not-callable
        formi18n = self.formi18n_class()  # pylint: disable=not-callable
        self.ctx['forms'] = [form, formi18n]
        self.ctx['action'] = reverse(self.action_url)
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        form = self.form_class(request.POST)  # pylint: disable=not-callable
        formi18n = self.formi18n_class(request.POST)  # pylint: disable=not-callable
        self.ctx['forms'] = [form, formi18n]
        return self.save_form(request, self.template_name, self.ctx, self.fk_field_name)


class Common2UpdateView(Common2Mixin, View):
    template_name = ''
    ctx = {
        'form_class': '',
        'title': '',
        'submit_name': '',
    }
    action_url = ''
    fk_field_name = ''
    reverse_field_name = ''

    def get(self, request, pk):
        model, modeli18n = self.get_models(pk, self.reverse_field_name)
        form = self.form_class(instance=model)  # pylint: disable=not-callable
        formi18n = self.formi18n_class(instance=modeli18n)  # pylint: disable=not-callable

        self.ctx['forms'] = [form, formi18n]
        self.ctx['action'] = reverse(self.action_url, kwargs={'pk': form.instance.pk}),
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        model, modeli18n = self.get_models(pk, self.reverse_field_name)
        form = self.form_class(request.POST, instance=model)  # pylint: disable=not-callable
        formi18n = self.formi18n_class(request.POST, instance=modeli18n)  # pylint: disable=not-callable
        self.ctx['forms'] = [form, formi18n]
        self.ctx['action'] = reverse(self.action_url, kwargs={'pk': form.instance.pk}),
        return self.save_form(request, self.template_name, self.ctx, self.fk_field_name)

class Common2DeleteView(View):
    model = None
    template_name = ''
    ctx = {
        'form_class': '',
        'title': '',
        'text': '',
        'submit_name': '',
    }
    action_url = ''

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        self.ctx['action'] = reverse(self.action_url, kwargs={'pk': pk})
        self.ctx['label'] = model_obj.pk
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        model_obj.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})      
