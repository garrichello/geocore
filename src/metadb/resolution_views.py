from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy

from .simple_forms import ResolutionForm

from .models import Resolution

class ResolutionBaseView(View):
    form_class = ResolutionForm
    model = Resolution

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


class ResolutionCreateView(ResolutionBaseView):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-resolution-create-form',
        'action': reverse_lazy('metadb:resolution_create'),
        'title': _("Create a new resolution"),
        'submit_name': _("Create resolution"),
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


class ResolutionUpdateView(ResolutionBaseView):
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-resolution-update-form',
        'title': _("Update resolution"),
        'submit_name': _("Update resolution"),
    }

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=model_obj)

        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse('metadb:resolution_update', kwargs={'pk': form.instance.pk})
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, instance=model_obj)
        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse('metadb:resolution_update', kwargs={'pk': form.instance.pk})
        return self.save_form(request, self.template_name, self.ctx)

class ResolutionDeleteView(ResolutionBaseView):
    template_name = 'metadb/includes/simple_delete_form.html'
    ctx = {
        'form_class': 'js-resolution-delete-form',
        'title': _('Confirm resolution delete'),
        'text': _('Are you sure you want to delete the resolution'),
        'submit_name': _('Delete resolution')
    }

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        self.ctx['action'] = reverse('metadb:resolution_delete', kwargs={'pk': pk})
        self.ctx['label'] = model_obj.label
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        model_obj.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})      
