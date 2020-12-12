from django.utils.translation import gettext_lazy as _

from .common2_views import Common2CreateView, Common2UpdateView, Common2DeleteView

from .simple_forms import OrganizationForm, OrganizationI18NForm

from .models import Organization


class OrganizationCreateView(Common2CreateView):
    form_class = OrganizationForm
    formi18n_class = OrganizationI18NForm
    model = Organization
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-organization-form',
        'title': _("Create a new organization"),
        'submit_name': _("Create organization"),
    }
    action_url = 'metadb:organization_create'
    fk_field_name = 'organization'


class OrganizationUpdateView(Common2UpdateView):
    form_class = OrganizationForm
    formi18n_class = OrganizationI18NForm
    model = Organization
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-organization-form',
        'title': _("Update organization"),
        'submit_name': _("Update organization"),
    }
    action_url = 'metadb:organization_update'
    fk_field_name = 'organization'
    reverse_field_name = 'organizationi18n'


class OrganizationDeleteView(Common2DeleteView):
    model = Organization
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-organization-delete-form',
        'title': _('Confirm organization delete'),
        'text': _('Are you sure you want to delete the organization'),
        'submit_name': _('Delete organization')
    }
    action_url = 'metadb:organization_delete'
