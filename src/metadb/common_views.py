from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import get_language

from .models import Language

class CommonBaseView(View):
    form_class = None
    model = None
    modeli18n = None
    template_name = ''
    ctx = {
        'form_class': '',
        'title': '',
        'submit_name': '',
        'script': '',
        'attributes': [
            {'name': '', 
             'value': ''},
        ]
    }
    action_url = ''
    create = False
    fk_field_name = ''
    i18n_field = 'name'  # Default field name!

    def save_valid_form(self, form):
        obj = form.save()
        qset = self.modeli18n.objects.filter(language__code=get_language()).filter(
            **{self.fk_field_name: obj})
        if qset.count() == 0:
            obji18n = self.modeli18n()  # If we've just created a new object  # pylint: disable=not-callable
        else:
            obji18n = qset.get()  # If it's an old one
        # NB! Here we set obj18n.name = form.cleaned_data['name']. 'name' (i18n_field) is used TWICE!
        setattr(obji18n, self.i18n_field, form.cleaned_data[self.i18n_field])
        setattr(obji18n, self.fk_field_name, obj)  # Link it with the new Parameter object
        # To save DB consistency we create a new record for all languages.
        # User can update/translate to every other language lately and separately.
        if self.create:
            for db_lang in Language.objects.all():  # Iterate over all languages in DB
                obji18n.language = db_lang  # Link it with an existing language
                obji18n.pk = None  # Clear PK to save data into a new record
                obji18n.save()  # Save
        else:  # Just update the existing record.
            obji18n.save()

    def save_form_old(self, request, template_name, ctx):
        ''' Saves the form
        For simple models
        '''
        data = dict()
        form = ctx['forms'][0]
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)

    def save_form(self, request, template_name, ctx):
        ''' Saves the form
        For internationalized models with fields placed into a single form.
        Primary model is the form's model. International model fields are added to the form.
        Internationalized field name is always 'name'. But can be changed if necessary.
        self.create -- True if creating, False if updating.
        fk_field_name - name of the FK field in the internationalized model.
        '''
        data = dict()
        form = ctx['forms'][0]
        if form.is_valid():
            if self.fk_field_name:
                self.save_valid_form(form)
            else:
                form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)

class CommonCreateView(CommonBaseView):
    create = True

    def get(self, request):
        form = self.form_class()  # pylint: disable=not-callable
        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse(self.action_url)
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        form = self.form_class(request.POST)  # pylint: disable=not-callable
        self.ctx['forms'] = [form]
        return self.save_form(request, self.template_name, self.ctx)


class CommonUpdateView(CommonBaseView):
    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=obj)  # pylint: disable=not-callable

        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse(self.action_url, kwargs={'pk': form.instance.pk})
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, instance=obj)  # pylint: disable=not-callable
        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse(self.action_url, kwargs={'pk': form.instance.pk})
        return self.save_form(request, self.template_name, self.ctx)


class CommonDeleteView(CommonBaseView):
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
