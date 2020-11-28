from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .resolution_forms import ResolutionForm

from .models import Resolution

class ResolutionBaseView(View):
    form_class = ResolutionForm
    model = Resolution

    def save_form(self, request, form, template_name):
        ''' Saves the form
        '''
        data = dict()
        if (True):
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
            else:
                data['form_is_valid'] = False

        ctx = {'forms': [form], 'pk': form.instance.pk}
        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)


class ResolutionCreateView(ResolutionBaseView):
    template_name = 'metadb/includes/resolution_create_form.html'

    def get(self, request):
        form = self.form_class()

        ctx = {'forms': [form]}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        form = self.form_class(request.POST)
        return self.save_form(request, form, self.template_name)


class ResolutionUpdateView(ResolutionBaseView):
    template_name = 'metadb/includes/resolution_update_form.html'

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=model_obj)

        ctx = {'forms': [form], 'pk': form.instance.pk}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, instance=model_obj)
        return self.save_form(request, form, self.template_name)

class ResolutionDeleteView(ResolutionBaseView):
    template_name = 'metadb/includes/resolution_delete_form.html'

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)

        ctx = {'resolution': model_obj}
        html_form = render_to_string(self.template_name, ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        model_obj.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})      
