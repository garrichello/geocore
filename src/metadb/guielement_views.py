from django.utils.translation import gettext_lazy as _

from .simple_forms import GuiElementForm, GuiElementI18NForm

from .models import GuiElement

from .common2_views import Common2CreateView, Common2UpdateView, Common2DeleteView


class GuiElementCreateView(Common2CreateView):
    form_class = GuiElementForm
    formi18n_class = GuiElementI18NForm
    model = GuiElement
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-gui-element-form',
        'title': _("Create a new GUI element"),
        'submit_name': _("Create GUI element"),
    }
    action_url = 'metadb:gui_element_create'
    fk_field_name = 'gui_element'


class GuiElementUpdateView(Common2UpdateView):
    form_class = GuiElementForm
    formi18n_class = GuiElementI18NForm
    model = GuiElement
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-gui-element-form',
        'title': _("Update GUI element"),
        'submit_name': _("Update GUI element"),
    }
    action_url = 'metadb:gui_element_update'
    fk_field_name = 'gui_element'
    reverse_field_name = 'guielementi18n'


class GuiElementDeleteView(Common2DeleteView):
    model = GuiElement
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-gui-element-delete-form',
        'title': _('Confirm GUI element delete'),
        'text': _('Are you sure you want to delete the GUI element'),
        'submit_name': _('Delete GUI element')
    }
    action_url = 'metadb:gui_element_delete'
