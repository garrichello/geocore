from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy

from .simple_forms import FileTypeForm

from .models import FileType

class FileTypeBaseView(View):
    form_class = FileTypeForm
    model = FileType

    def save_form(self, request, template_name, ctx):
        ''' Saves the form
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


class FileTypeCreateView(FileTypeBaseView):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-filetype-create-form',
        'action': reverse_lazy('metadb:filetype_create'),
        'title': _("Create a new file type"),
        'submit_name': _("Create file type"),
    }

    def get(self, request):
        form = self.form_class()

        self.ctx['forms'] = [form]
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        form = self.form_class(request.POST)
        self.ctx['forms'] = [form]
        return self.save_form(request, self.template_name, self.ctx)


class FileTypeUpdateView(FileTypeBaseView):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-filetype-update-form',
        'title': _("Update file type"),
        'submit_name': _("Update file type"),
    }

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=model_obj)

        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse('metadb:filetype_update', kwargs={'pk': form.instance.pk})
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, instance=model_obj)
        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse('metadb:filetype_update', kwargs={'pk': form.instance.pk})
        return self.save_form(request, self.template_name, self.ctx)

class FileTypeDeleteView(FileTypeBaseView):
    template_name = 'metadb/includes/simple_delete_form.html'
    ctx = {
        'form_class': 'js-filetype-delete-form',
        'title': _('Confirm file type delete'),
        'text': _('Are you sure you want to delete the file type'),
        'submit_name': _('Delete file type')
    }

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        self.ctx['action'] = reverse('metadb:filetype_delete', kwargs={'pk': pk})
        self.ctx['label'] = model_obj.label
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        model_obj.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})      
