from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .common_views import CommonCreateView, CommonUpdateView, CommonDeleteView

from .simple_forms import *

from .models import *


class AccumulationModeCreateView(CommonCreateView):
    form_class = AccumulationModeForm
    model = AccumulationMode
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-accmode-form',
        'title': _("Create a new accumulation mode"),
        'submit_name': _("Create accumulation mode"),
    }
    url_name = 'metadb:accmode_create'


class AccumulationModeUpdateView(CommonUpdateView):
    form_class = AccumulationModeForm
    model = AccumulationMode
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-accmode-form',
        'title': _("Update accumulation mode"),
        'submit_name': _("Update accumulation mode"),
    }
    url_name = 'metadb:accmode_update'


class AccumulationModeDeleteView(CommonDeleteView):
    form_class = AccumulationModeForm
    model = AccumulationMode
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-accmode-delete-form',
        'title': _('Confirm accumulation mode delete'),
        'text': _('Are you sure you want to delete the accumulation mode'),
        'submit_name': _('Delete accumulation mode')
    }
    url_name = 'metadb:accmode_delete'


class DataKindCreateView(CommonCreateView):
    form_class = DataKindForm
    model = DataKind
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-datakind-form',
        'title': _("Create a new datakind"),
        'submit_name': _("Create datakind"),
    }
    url_name = 'metadb:datakind_create'


class DataKindUpdateView(CommonUpdateView):
    form_class = DataKindForm
    model = DataKind
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-datakind-form',
        'title': _("Update datakind"),
        'submit_name': _("Update datakind"),
    }
    url_name = 'metadb:datakind_update'


class DataKindDeleteView(CommonDeleteView):
    form_class = DataKindForm
    model = DataKind
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-datakind-delete-form',
        'title': _('Confirm data kind delete'),
        'text': _('Are you sure you want to delete the data kind'),
        'submit_name': _('Delete data kind')
    }
    url_name = 'metadb:datakind_delete'


class FileCreateView(CommonCreateView):
    form_class = FileForm
    model = File
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-file-form',
        'title': _("Create a new file"),
        'submit_name': _("Create file"),
    }
    url_name = 'metadb:file_create'


class FileUpdateView(CommonUpdateView):
    form_class = FileForm
    model = File
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-file-form',
        'title': _("Update file"),
        'submit_name': _("Update file"),
    }
    url_name = 'metadb:file_update'


class FileDeleteView(CommonDeleteView):
    form_class = FileForm
    model = File
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-file-delete-form',
        'title': _('Confirm file delete'),
        'text': _('Are you sure you want to delete the file'),
        'submit_name': _('Delete file')
    }
    url_name = 'metadb:file_delete'


class FileTypeCreateView(CommonCreateView):
    form_class = FileTypeForm
    model = FileType
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-filetype-form',
        'title': _("Create a new filetype"),
        'submit_name': _("Create filetype"),
    }
    url_name = 'metadb:filetype_create'


class FileTypeUpdateView(CommonUpdateView):
    form_class = FileTypeForm
    model = FileType
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-filetype-form',
        'title': _("Update filetype"),
        'submit_name': _("Update filetype"),
    }
    url_name = 'metadb:filetype_update'


class FileTypeDeleteView(CommonDeleteView):
    form_class = FileTypeForm
    model = FileType
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-filetype-delete-form',
        'title': _('Confirm file type delete'),
        'text': _('Are you sure you want to delete the file type'),
        'submit_name': _('Delete file type')
    }
    url_name = 'metadb:filetype_delete'


class LanguageCreateView(CommonCreateView):
    form_class = LanguageForm
    model = Language
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-language-form',
        'title': _("Create a new language"),
        'submit_name': _("Create language"),
    }
    url_name = 'metadb:language_create'


class LanguageUpdateView(CommonUpdateView):
    form_class = LanguageForm
    model = Language
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-language-form',
        'title': _("Update language"),
        'submit_name': _("Update language"),
    }
    url_name = 'metadb:language_update'


class LanguageDeleteView(CommonDeleteView):
    form_class = LanguageForm
    model = Language
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-language-delete-form',
        'title': _('Confirm language delete'),
        'text': _('Are you sure you want to delete the language'),
        'submit_name': _('Delete language')
    }
    url_name = 'metadb:language_delete'


class LevelsVariableCreateView(CommonCreateView):
    form_class = LevelsVariableForm
    model = Variable
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-levels-variable-form',
        'title': _("Create a new levels variable"),
        'submit_name': _("Create levels variable"),
    }
    url_name = 'metadb:levels_variable_create'


class LevelsVariableUpdateView(CommonUpdateView):
    form_class = LevelsVariableForm
    model = Variable
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-levels-variable-form',
        'title': _("Update levels variable"),
        'submit_name': _("Update levels variable"),
    }
    url_name = 'metadb:levels_variable_update'

class LevelsVariableDeleteView(CommonDeleteView):
    form_class = LevelsVariableForm
    model = Variable
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-levels-variable-delete-form',
        'title': _('Confirm levels variable delete'),
        'text': _('Are you sure you want to delete the levels variable'),
        'submit_name': _('Delete levels variable')
    }
    url_name = 'metadb:levels_variable_delete'
    
    
class PropertyCreateView(CommonCreateView):
    form_class = PropertyForm
    model = Property
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-property-form',
        'title': _("Create a new property"),
        'submit_name': _("Create property"),
        'script': 'metadb/property_form.js',
        'attributes': [
            {'name': 'gui-element-url', 
             'value': reverse_lazy('metadb:form_load_guielements')},
        ],
    }
    url_name = 'metadb:property_create'


class PropertyUpdateView(CommonUpdateView):
    form_class = PropertyForm
    model = Property
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-property-form',
        'title': _("Update property"),
        'submit_name': _("Update property"),
        'script': 'metadb/property_form.js',
        'attributes': [
            {'name': 'gui-element-url', 
             'value': reverse_lazy('metadb:form_load_guielements')},
        ],
    }
    url_name = 'metadb:property_update'


class PropertyDeleteView(CommonDeleteView):
    form_class = PropertyForm
    model = Property
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-property-delete-form',
        'title': _('Confirm property delete'),
        'text': _('Are you sure you want to delete the property'),
        'submit_name': _('Delete property')
    }
    url_name = 'metadb:property_delete'


class PropertyValueCreateView(CommonCreateView):
    form_class = PropertyValueForm
    model = PropertyValue
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-property-value-form',
        'title': _("Create a new property value"),
        'submit_name': _("Create property value"),
    }
    url_name = 'metadb:property_value_create'


class PropertyValueUpdateView(CommonUpdateView):
    form_class = PropertyValueForm
    model = PropertyValue
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-property-value-form',
        'title': _("Update property value"),
        'submit_name': _("Update property value"),
    }
    url_name = 'metadb:property_value_update'


class PropertyValueDeleteView(CommonDeleteView):
    form_class = PropertyValueForm
    model = PropertyValue
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-property-value-delete-form',
        'title': _('Confirm property value delete'),
        'text': _('Are you sure you want to delete the property value'),
        'submit_name': _('Delete property value')
    }
    url_name = 'metadb:property_value_delete'


class ResolutionCreateView(CommonCreateView):
    form_class = ResolutionForm
    model = Resolution
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-resolution-form',
        'title': _("Create a new resolution"),
        'submit_name': _("Create resolution"),
    }
    url_name = 'metadb:resolution_create'


class ResolutionUpdateView(CommonUpdateView):
    form_class = ResolutionForm
    model = Resolution
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-resolution-form',
        'title': _("Update resolution"),
        'submit_name': _("Update resolution"),
    }
    url_name = 'metadb:resolution_update'


class ResolutionDeleteView(CommonDeleteView):
    form_class = ResolutionForm
    model = Resolution
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-resolution-delete-form',
        'title': _('Confirm resolution delete'),
        'text': _('Are you sure you want to delete the resolution'),
        'submit_name': _('Delete resolution')
    }
    url_name = 'metadb:resolution_delete'


class RootDirCreateView(CommonCreateView):
    form_class = RootDirForm
    model = RootDir
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-root-dir-form',
        'title': _("Create a new root directory"),
        'submit_name': _("Create root directory"),
    }
    url_name = 'metadb:root_dir_create'


class RootDirUpdateView(CommonUpdateView):
    form_class = RootDirForm
    model = RootDir
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-root-dir-form',
        'title': _("Update root directory"),
        'submit_name': _("Update root directory"),
    }
    url_name = 'metadb:root_dir_update'


class RootDirDeleteView(CommonDeleteView):
    form_class = RootDirForm
    model = RootDir
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-root-dir-delete-form',
        'title': _('Confirm root directory delete'),
        'text': _('Are you sure you want to delete the root directory'),
        'submit_name': _('Delete root directory')
    }
    url_name = 'metadb:root_dir_delete'


class ScenarioCreateView(CommonCreateView):
    form_class = ScenarioForm
    model = Scenario
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-scenario-form',
        'title': _("Create a new scenario"),
        'submit_name': _("Create scenario"),
    }
    url_name = 'metadb:scenario_create'


class ScenarioUpdateView(CommonUpdateView):
    form_class = ScenarioForm
    model = Scenario
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-scenario-form',
        'title': _("Update scenario"),
        'submit_name': _("Update scenario"),
    }
    url_name = 'metadb:scenario_update'


class ScenarioDeleteView(CommonDeleteView):
    form_class = ScenarioForm
    model = Scenario
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-scenario-delete-form',
        'title': _('Confirm scenario delete'),
        'text': _('Are you sure you want to delete the scenario'),
        'submit_name': _('Delete scenario')
    }
    url_name = 'metadb:scenario_delete'


class VariableCreateView(CommonCreateView):
    form_class = VariableForm
    model = Variable
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-variable-form',
        'title': _("Create a new variable"),
        'submit_name': _("Create variable"),
    }
    url_name = 'metadb:variable_create'


class VariableUpdateView(CommonUpdateView):
    form_class = VariableForm
    model = Variable
    template_name = 'metadb/includes/simple_form.html'
    ctx = {
        'form_class': 'js-variable-form',
        'title': _("Update variable"),
        'submit_name': _("Update variable"),
    }
    url_name = 'metadb:variable_update'


class VariableDeleteView(CommonDeleteView):
    form_class = VariableForm
    model = Variable
    template_name = 'metadb/includes/delete_form.html'
    ctx = {
        'form_class': 'js-variable-delete-form',
        'title': _('Confirm variable delete'),
        'text': _('Are you sure you want to delete the variable'),
        'submit_name': _('Delete variable')
    }
    url_name = 'metadb:variable_delete'
