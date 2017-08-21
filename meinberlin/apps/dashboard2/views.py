from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views import generic

from adhocracy4.modules import models as module_models
from adhocracy4.phases import models as phase_models
from adhocracy4.projects import models as project_models

from . import blueprints
from . import forms
from . import mixins
from .contents import content

User = get_user_model()


def get_object_or_none(*args, **kwargs):
    try:
        return get_object_or_404(*args, **kwargs)
    except Http404:
        return None


class ProjectListView(mixins.DashboardBaseMixin,
                      generic.ListView):
    model = project_models.Project
    paginate_by = 12
    template_name = 'meinberlin_dashboard2/project_list.html'
    permission_required = 'a4projects.add_project'

    def get_queryset(self):
        return super().get_queryset().filter(
            organisation=self.organisation
        )


class BlueprintListView(mixins.DashboardBaseMixin,
                        generic.TemplateView):
    blueprints = blueprints.blueprints
    template_name = 'meinberlin_dashboard2/blueprint_list.html'
    permission_required = 'a4projects.add_project'
    menu_item = 'project'


class ProjectCreateView(mixins.DashboardBaseMixin,
                        mixins.BlueprintMixin,
                        generic.CreateView,
                        SuccessMessageMixin):
    model = project_models.Project
    form_class = forms.ProjectCreateForm
    template_name = 'meinberlin_dashboard2/project_create_form.html'
    permission_required = 'a4projects.add_project'
    success_message = _('Project succesfully created.')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['type'] = self.blueprint_key
        kwargs['organisation'] = self.organisation
        kwargs['creator'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('a4dashboard:project-edit',
                       kwargs={'project_slug': self.object.slug})

    def form_valid(self, form):
        response = super().form_valid(form)

        # FIXME: maybe replace by dashboard signals
        self._create_modules_and_phases(self.object)

        return response

    def _create_modules_and_phases(self, project):
        module = module_models.Module(
            name=project.slug + '_module',
            weight=1,
            project=project,
        )
        module.save()
        self._create_phases(module, self.blueprint.content)

    def _create_phases(self, module, blueprint_phases):
        for phase_content in blueprint_phases:
            phase = phase_models.Phase(
                type=phase_content.identifier,
                name=phase_content.name,
                description=phase_content.description,
                weight=phase_content.weight,
                module=module,
            )
            phase.save()


class ProjectUpdateView(mixins.DashboardBaseMixin,
                        generic.UpdateView,
                        SuccessMessageMixin):
    model = project_models.Project
    slug_url_kwarg = 'project_slug'
    form_class = forms.ProjectUpdateForm
    template_name = 'meinberlin_dashboard2/project_update_form.html'
    permission_required = 'a4projects.add_project'
    success_message = _('Project successfully created.')


class ProjectComponentDispatcher(mixins.DashboardComponentMixin,
                                 generic.View):
    def get(self, request, *args, **kwargs):
        component = self.get_component()
        if not component:
            raise Http404('Component not found')

        kwargs['module'] = None
        kwargs['project'] = self.project
        return component.get_view()(request, *args, **kwargs)

    post = get

    def get_component(self):
        if 'component_identifier' not in self.kwargs:
            return None
        if self.kwargs['component_identifier'] not in content.projects:
            return None
        return content.projects[self.kwargs['component_identifier']]


class ModuleComponentDispatcher(mixins.DashboardComponentMixin,
                                generic.View):

    def get(self, request, *args, **kwargs):
        component = self.get_component()
        if not component:
            raise Http404('Component not found')

        kwargs['module'] = self.module
        kwargs['project'] = self.module.project

        return component.get_view()(request, *args, **kwargs)

    post = get

    def get_component(self):
        if 'component_identifier' not in self.kwargs:
            return None
        if self.kwargs['component_identifier'] not in content.modules:
            return None
        return content.modules[self.kwargs['component_identifier']]


class ProjectComponentFormView(mixins.DashboardComponentMixin,
                               mixins.DashboardBaseMixin,
                               mixins.DashboardContextMixin,
                               SuccessMessageMixin,
                               generic.UpdateView):

    permission_required = 'a4projects.add_project'
    model = project_models.Project
    template_name = 'meinberlin_dashboard2/base_form_project.html'
    success_message = _('Project successfully updated.')

    # Properties to be set when calling as_view()
    component = None
    title = ''
    form_class = None
    form_template_name = ''

    def get_object(self, queryset=None):
        return self.project


class ModuleComponentFormView(mixins.DashboardComponentMixin,
                              mixins.DashboardBaseMixin,
                              mixins.DashboardContextMixin,
                              SuccessMessageMixin,
                              generic.UpdateView):

    permission_required = 'a4projects.add_project'
    model = module_models.Module
    template_name = 'meinberlin_dashboard2/base_form_module.html'
    success_message = _('Module successfully updated.')

    # Properties to be set when calling as_view()
    component = None
    title = ''
    form_class = None
    form_template_name = ''

    def get_object(self, queryset=None):
        return self.module
