from django.conf import settings
from django.dispatch import receiver
from django.utils import translation
from django.utils.translation import ugettext as _

from meinberlin.apps.dashboard2 import signals as a4dashboard_signals

from . import models


@receiver(a4dashboard_signals.module_component_updated)
def log_module_component_changes(sender, module, component, user, **kwargs):
    with translation.override(settings.DEFAULT_LANGUAGE):
        message = _(
            'The component "{component_label}"'
            ' in the module "{module_name}"'
            ' of the project "{project_name}" has been modified.').format(
                project_name=module.project.name,
                module_name=module.name,
                component_label=component.label)

    models.LogEntry.objects.create(
        message=message,
        action=models.MODULE_COMPONENT_UPDATED,
        actor=user,
        component_identifier=component.identifier,
        project=module.project,
        module=module,
    )


@receiver(a4dashboard_signals.project_component_updated)
def log_project_component_changes(sender, project, component, user, **kwargs):
    with translation.override(settings.DEFAULT_LANGUAGE):
        message = _(
            'The component "{component_label}"'
            ' of the project "{project_name}" has been modified.').format(
                project_name=project.name,
                component_label=component.label)

    models.LogEntry.objects.create(
        message=message,
        action=models.PROJECT_COMPONENT_UPDATED,
        actor=user,
        component_identifier=component.identifier,
        project=project,
        module=None
    )


@receiver(a4dashboard_signals.project_created)
def log_project_created(sender, project, user, **kwargs):
    with translation.override(settings.DEFAULT_LANGUAGE):
        message = _(
            'The project "{project_name}" has been created.').format(
                project_name=project.name)

    models.LogEntry.objects.create(
        message=message,
        action=models.PROJECT_CREATED,
        actor=user,
        project=project,
        module=None,
        component_identifier=''
    )


@receiver(a4dashboard_signals.project_published)
def log_project_published(sender, project, user, **kwargs):
    with translation.override(settings.DEFAULT_LANGUAGE):
        message = _(
            'The project "{project_name}" has been published.').format(
                project_name=project.name)

    models.LogEntry.objects.create(
        message=message,
        action=models.PROJECT_PUBLISHED,
        actor=user,
        project=project,
        module=None,
        component_identifier=''
    )


@receiver(a4dashboard_signals.project_unpublished)
def log_project_unpublished(sender, project, user, **kwargs):
    with translation.override(settings.DEFAULT_LANGUAGE):
        message = _(
            'The project "{project_name}" has been unpublished.').format(
                project_name=project.name)

    models.LogEntry.objects.create(
        message=message,
        action=models.PROJECT_UNPUBLISHED,
        actor=user,
        project=project,
        module=None,
        component_identifier=''
    )
