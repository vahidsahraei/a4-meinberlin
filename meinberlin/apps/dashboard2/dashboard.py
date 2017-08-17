from django.utils.translation import ugettext_lazy as _

from . import ModuleFormComponent
from . import ProjectFormComponent
from . import content
from . import forms
from .apps import Config


class ProjectBasicComponent(ProjectFormComponent):
    app_label = Config.label
    label = 'basic'
    identifier = 'basic'

    menu_label = _('Basic settings')
    form_title = _('Edit basic settings')
    form_class = forms.ProjectBasicForm
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/project_basic_form.html'


class ProjectInformationComponent(ProjectFormComponent):
    app_label = Config.label
    label = 'information'
    identifier = 'information'

    menu_label = _('Information')
    form_title = _('Edit project information')
    form_class = forms.ProjectInformationForm
    form_template_name = 'meinberlin_dashboard2' \
                         '/includes/project_information_form.html'


class ModuleBasicComponent(ModuleFormComponent):
    app_label = Config.label
    label = 'phases'
    identifier = 'module_basic'

    menu_label = _('Basic information')
    form_title = _('Edit basic module information')
    form_class = forms.ModuleBasicForm
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/module_basic_form.html'


class ModulePhasesComponent(ModuleFormComponent):
    app_label = Config.label
    label = 'phases'
    identifier = 'phases'

    menu_label = _('Phases')
    form_title = _('Edit phases information')
    form_class = forms.PhaseFormSet
    form_template_name = 'meinberlin_dashboard2/includes' \
                         '/module_phases_form.html'


content.register_project(ProjectBasicComponent())
content.register_project(ProjectInformationComponent())
content.register_module(ModuleBasicComponent())
content.register_module(ModulePhasesComponent())
