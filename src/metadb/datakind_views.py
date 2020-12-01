from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy

from .datakind_forms import DataKindForm

from .models import DataKind

class DataKindBaseView(View):
    form_class = DataKindForm
    model = DataKind

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


class DataKindCreateView(DataKindBaseView):
    template_name = 'metadb/includes/datakind_form.html'
    ctx = {
        'form_class': 'js-datakind-create-form',
        'action': reverse_lazy('metadb:datakind_create'),
        'title': _("Create a new data kind"),
        'submit_name': _("Create data kind"),
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


class DataKindUpdateView(DataKindBaseView):
    template_name = 'metadb/includes/datakind_form.html'
    ctx = {
        'form_class': 'js-datakind-update-form',
        'title': _("Update data kind"),
        'submit_name': _("Update data kind"),
    }

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=model_obj)

        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse('metadb:datakind_create', kwargs={'pk': form.instance.pk})
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, instance=model_obj)
        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse('metadb:datakind_create', kwargs={'pk': form.instance.pk})
        return self.save_form(request, self.template_name, self.ctx)

class DataKindDeleteView(DataKindBaseView):
    template_name = 'metadb/includes/datakind_delete_form.html'

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)

        ctx = {'datakind': model_obj}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        model_obj.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})      
