from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse


class SimpleBaseView(View):
    form_class = None
    model = None

    def save_form(self, request, template_name, ctx):
        ''' Saves the form '''
        data = dict()
        form = ctx['forms'][0]
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

        data['html_form'] = render_to_string(template_name, ctx, request)
        return JsonResponse(data)


class SimpleCreateView(SimpleBaseView):
    template_name = ''
    ctx = {}
    url_name = ''

    def get(self, request):
        form = self.form_class()  # pylint: disable=not-callable
        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse(self.url_name)
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request):
        form = self.form_class(request.POST)  # pylint: disable=not-callable
        self.ctx['forms'] = [form]
        return self.save_form(request, self.template_name, self.ctx)


class SimpleUpdateView(SimpleBaseView):
    template_name = ''
    ctx = {}
    url_name = ''

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=obj)  # pylint: disable=not-callable

        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse(self.url_name, kwargs={'pk': form.instance.pk})
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(request.POST, instance=obj)  # pylint: disable=not-callable
        self.ctx['forms'] = [form]
        self.ctx['action'] = reverse(self.url_name, kwargs={'pk': form.instance.pk})
        return self.save_form(request, self.template_name, self.ctx)


class SimpleDeleteView(SimpleBaseView):
    template_name = ''
    ctx = {}
    url_name = ''

    def get(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        self.ctx['action'] = reverse(self.url_name, kwargs={'pk': pk})
        self.ctx['label'] = model_obj.pk
        html_form = render_to_string(self.template_name, self.ctx, request)
        return JsonResponse({'html_form': html_form})

    def post(self, request, pk):
        model_obj = get_object_or_404(self.model, pk=pk)
        model_obj.delete()
        return JsonResponse({'html_form': None, 'form_is_valid': True})
