import json

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from easy_thumbnails.files import get_thumbnailer

from adhocracy4.dashboard import mixins as a4dashboard_mixins
from adhocracy4.exports import mixins as export_mixins
from adhocracy4.exports import unescape_and_strip_html
from adhocracy4.exports import views as export_views
from adhocracy4.rules import mixins as rules_mixins
from meinberlin.apps.contrib.views import CanonicalURLDetailView
from meinberlin.apps.maps.models import MapPreset
from meinberlin.apps.plans.forms import PlanForm
from meinberlin.apps.plans.models import Plan
from meinberlin.apps.projects.models import Project

from . import models


class PlanDetailView(rules_mixins.PermissionRequiredMixin,
                     CanonicalURLDetailView):
    model = models.Plan
    template_name = 'meinberlin_plans/plan_detail.html'
    permission_required = 'meinberlin_plans.view_plan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['berlin_polygon'] = settings.BERLIN_POLYGON
        return context


class PlanListView(rules_mixins.PermissionRequiredMixin,
                   generic.ListView):
    model = models.Plan
    template_name = 'meinberlin_plans/plan_list.html'
    permission_required = 'meinberlin_plans.list_plan'

    def get_districts(self):
        try:
            return MapPreset.objects.filter(
                category__name='Bezirke - Berlin')
        except ObjectDoesNotExist:
            return []

    def _get_status_string(self, projects):

        future_phase = None
        for project in projects:
            phases = project.phases
            if phases.active_phases():
                return ugettext('running')
            if phases.future_phases() and \
               phases.future_phases().first().start_date:
                date = phases.future_phases().first().start_date
                if not future_phase:
                    future_phase = date
                else:
                    if date < future_phase:
                        future_phase = date

        if future_phase:
            return ugettext('starts at {}').format(future_phase.date())

    def _get_participation_status(self, item):
        projects = item.projects.all()\
            .filter(is_draft=False,
                    is_archived=False,
                    is_public=True)
        if not projects:
            return item.get_participation_display(), False
        else:
            status_string = self._get_status_string(projects)
            if status_string:
                return status_string, True
            else:
                return item.get_participation_display(), False

    def _get_participation_status_project(self, project):
        if project.phases.active_phases():
            return ugettext('running'), True
        elif project.phases.future_phases():
            try:
                return (ugettext('starts at {}').format
                        (project.phases.future_phases().first().
                         start_date.date()),
                        True)
            except AttributeError:
                return (ugettext('starts in the future'),
                        True)
        else:
            return ugettext('done'), False

    def _get_status_project(self, project):
        if project.phases.active_phases() or project.phases.future_phases():
            return 2, ugettext('Implementation')
        else:
            return 3, ugettext('Done')

    def _get_phase_status(self, project):
        if (project.future_phases and
                project.future_phases.first().start_date):
            date_str = str(
                project.future_phases.first().start_date.date())
            return (date_str,
                    False,
                    False)
        elif project.active_phase:
            progress = project.active_phase_progress
            time_left = project.time_left
            return (False,
                    [progress, time_left],
                    False)
        elif project.phases.past_phases():
            return (False,
                    False,
                    True)
        return (False,
                False,
                False)

    def get_context_data(self, **kwargs):

        city_wide = _('City wide')

        context = super().get_context_data(**kwargs)

        districts = self.get_districts()

        district_list = json.dumps([district.polygon
                                    for district in districts])
        district_names_list = [district.name
                               for district in districts]
        district_names_list.append(str(city_wide))
        district_names = json.dumps(district_names_list)
        context['districts'] = district_list
        context['district_names'] = district_names

        topics = getattr(settings, 'A4_PROJECT_TOPICS', None)
        if topics:
            topics = dict((x, str(y)) for x, y in topics)
        else:
            raise ImproperlyConfigured('set A4_PROJECT_TOPICS in settings')
        context['topic_choices'] = json.dumps(topics)

        items = sorted(context['object_list'],
                       key=lambda x: x.modified or x.created,
                       reverse=True)

        result = []

        for item in items:
            participation_string, active = self._get_participation_status(item)
            district_name = str(city_wide)
            if item.district:
                district_name = item.district.name

            result.append({
                'type': 'plan',
                'title': item.title,
                'url': item.get_absolute_url(),
                'organisation': item.organisation.name,
                'point': item.point,
                'point_label': item.point_label,
                'cost': item.cost,
                'district': district_name,
                'topic': item.theme,
                'status': item.status,
                'status_display': item.get_status_display(),
                'participation_string': participation_string,
                'participation_active': active,
                'participation': item.participation,
                'participation_display': item.get_participation_display(),
                'published_projects_count': item.published_projects.count(),
            })

        projects = Project.objects.all()\
            .filter(is_draft=False, is_archived=False)\
            .order_by('created')

        for item in projects:
            if self.request.user.has_perm('a4projects.view_project', item):
                district_name = str(city_wide)
                if item.administrative_district:
                    district_name = item.administrative_district.name
                point = item.point
                if not point:
                    point = ''
                point_label = ''
                cost = ''
                participation_string, active = \
                    self._get_participation_status_project(item)
                status, status_display = \
                    self._get_status_project(item)
                participation = 1
                participation_display = _('Yes')
                future_phase, active_phase, past_phase = \
                    self._get_phase_status(item)
                image_url = ''
                if item.tile_image:
                    image = get_thumbnailer(item.tile_image)['project_tile']
                    image_url = image.url

                result.append({
                    'type': 'project',
                    'title': item.name,
                    'url': item.get_absolute_url(),
                    'organisation': item.organisation.name,
                    'tile_image': image_url,
                    'tile_image_copyright': item.tile_image_copyright,
                    'point': point,
                    'point_label': point_label,
                    'cost': cost,
                    'district': district_name,
                    'topic': item.topic,
                    'status': status,
                    'status_display': str(status_display),
                    'participation_string': str(participation_string),
                    'participation_active': active,
                    'participation': participation,
                    'participation_display': str(participation_display),
                    'description': item.description,
                    'future_phase': future_phase,
                    'active_phase': active_phase,
                    'past_phase': past_phase
                })

        context['items'] = json.dumps(result)
        context['baseurl'] = settings.A4_MAP_BASEURL
        context['attribution'] = settings.A4_MAP_ATTRIBUTION
        context['bounds'] = json.dumps(settings.A4_MAP_BOUNDING_BOX)
        context['district'] = self.request.GET.get('district', -1)
        context['topic'] = self.request.GET.get('topic', -1)

        return context


class PlanExportView(rules_mixins.PermissionRequiredMixin,
                     export_mixins.ItemExportWithLinkMixin,
                     export_mixins.ExportModelFieldsMixin,
                     export_mixins.ItemExportWithLocationMixin,
                     export_views.BaseExport,
                     export_views.AbstractXlsxExportView):

    permission_required = 'meinberlin_plans.list_plan'
    model = models.Plan
    fields = ['title', 'organisation', 'contact', 'district', 'cost',
              'description', 'theme', 'status', 'participation']
    html_fields = ['description']

    def get_object_list(self):
        return models.Plan.objects.all()

    def get_base_filename(self):
        return 'plans_%s' % timezone.now().strftime('%Y%m%dT%H%M%S')

    def get_virtual_fields(self, virtual):
        virtual = super().get_virtual_fields(virtual)
        virtual['projects'] = ugettext('Projects')
        virtual['projects_links'] = ugettext('Project Links')
        return virtual

    def get_organisation_data(self, item):
        return item.organisation.name

    def get_district_data(self, item):
        return item.district.name if item.district else str(_('City wide'))

    def get_contact_data(self, item):
        return unescape_and_strip_html(item.contact)

    def get_status_data(self, item):
        return item.get_status_display()

    def get_participation_data(self, item):
        return item.get_participation_display()

    def get_description_data(self, item):
        return unescape_and_strip_html(item.description)

    def get_projects_data(self, item):
        if item.projects.all():
            return ', \n'.join(
                [project.name
                 for project in item.projects.all()]
            )
        return ''

    def get_projects_links_data(self, item):
        if item.projects.all():
            return str([self.request.build_absolute_uri(
                        project.get_absolute_url())
                        for project in item.projects.all()
                        ])
        return ''


class DashboardPlanListView(a4dashboard_mixins.DashboardBaseMixin,
                            generic.ListView):
    model = Plan
    template_name = 'meinberlin_plans/plan_dashboard_list.html'
    permission_required = 'meinberlin_plans.add_plan'
    menu_item = 'project'

    def get_permission_object(self):
        return self.organisation

    def get_queryset(self):
        return super().get_queryset().filter(organisation=self.organisation)


class DashboardPlanCreateView(a4dashboard_mixins.DashboardBaseMixin,
                              generic.CreateView):
    model = Plan
    form_class = PlanForm
    permission_required = 'meinberlin_plans.add_plan'
    template_name = 'meinberlin_plans/plan_create_form.html'
    menu_item = 'project'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.organisation = self.organisation
        return super().form_valid(form)

    def get_permission_object(self):
        return self.organisation

    def get_success_url(self):
        return reverse(
            'a4dashboard:plan-list',
            kwargs={'organisation_slug': self.organisation.slug})


class DashboardPlanUpdateView(a4dashboard_mixins.DashboardBaseMixin,
                              generic.UpdateView):
    model = Plan
    form_class = PlanForm
    permission_required = 'meinberlin_plans.change_plan'
    template_name = 'meinberlin_plans/plan_update_form.html'
    menu_item = 'project'

    def get_permission_object(self):
        return self.organisation

    def get_success_url(self):
        return reverse(
            'a4dashboard:plan-list',
            kwargs={'organisation_slug': self.organisation.slug})


class DashboardPlanDeleteView(a4dashboard_mixins.DashboardBaseMixin,
                              generic.DeleteView):
    model = Plan
    success_message = _('The plan has been deleted')
    permission_required = 'meinberlin_plans.change_plan'
    template_name = 'meinberlin_plans/plan_confirm_delete.html'
    menu_item = 'project'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_permission_object(self):
        return self.organisation

    def get_success_url(self):
        return reverse(
            'a4dashboard:plan-list',
            kwargs={'organisation_slug': self.organisation.slug})
