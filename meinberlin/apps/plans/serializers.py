from django.utils.translation import ugettext as _
from easy_thumbnails.files import get_thumbnailer
from rest_framework import serializers

from adhocracy4.projects.models import Project
from meinberlin.apps.projects import get_project_type

from .models import Plan


class CommonFields:

    def get_district(self, instance):
        city_wide = _('City wide')
        district_name = str(city_wide)
        if instance.administrative_district:
            district_name = instance.administrative_district.name
        return district_name

    def get_point(self, instance):
        point = instance.point
        if not point:
            point = ''
        return point


class ProjectSerializer(serializers.ModelSerializer, CommonFields):
    type = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    organisation = serializers.SerializerMethodField()
    point = serializers.SerializerMethodField()
    point_label = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    participation = serializers.SerializerMethodField()
    participation_active = serializers.SerializerMethodField()
    participation_string = serializers.SerializerMethodField()
    participation_display = serializers.SerializerMethodField()
    future_phase = serializers.SerializerMethodField()
    active_phase = serializers.SerializerMethodField()
    past_phase = serializers.SerializerMethodField()
    tile_image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['type', 'title', 'url',
                  'organisation', 'tile_image',
                  'tile_image_copyright',
                  'point', 'point_label', 'cost',
                  'district', 'topic',
                  'status', 'status_display',
                  'participation_string',
                  'participation_active',
                  'participation', 'participation_display', 'description',
                  'future_phase', 'active_phase',
                  'past_phase']

    def _get_participation_status_project(self, instance):
        if instance.phases.active_phases():
            return _('running'), True
        elif instance.phases.future_phases():
            try:
                return (_('starts at {}').format
                        (instance.phases.future_phases().first().
                         start_date.date()),
                        True)
            except AttributeError:
                return (_('starts in the future'),
                        True)
        else:
            return _('done'), False

    def get_type(self, instance):
        return 'project'

    def get_title(self, instance):
        return instance.name

    def get_url(self, instance):
        if get_project_type(instance) in ('external', 'bplan'):
            return instance.externalproject.url
        return instance.get_absolute_url()

    def get_organisation(self, instance):
        return instance.organisation.name

    def get_tile_image(self, instance):
        image_url = ''
        if instance.tile_image:
            image = get_thumbnailer(instance.tile_image)['project_tile']
            image_url = image.url
        return image_url

    def get_point_label(self, instance):
        return ''

    def get_cost(self, instance):
        return ''

    def get_status(self, instance):
        if instance.phases.active_phases() or instance.phases.future_phases():
            return 2
        return 3

    def get_status_display(self, instance):
        if instance.phases.active_phases() or instance.phases.future_phases():
            return _('Implementation')
        return _('Done')

    def get_participation(self, instance):
        return 1

    def get_participation_display(self, instance):
        return _('Yes')

    def get_future_phase(self, instance):
        if (instance.future_phases and
                instance.future_phases.first().start_date):
            return str(
                instance.future_phases.first().start_date.date())
        return False

    def get_active_phase(self, instance):
        if instance.active_phase:
            progress = instance.active_phase_progress
            time_left = instance.time_left
            return [progress, time_left]
        return False

    def get_past_phase(self, instance):
        if instance.phases.past_phases():
            return True
        return False

    def get_participation_string(self, instance):
        participation_string, active = \
            self._get_participation_status_project(instance)
        return str(participation_string)

    def get_participation_active(self, instance):
        participation_string, active = \
            self._get_participation_status_project(instance)
        return active


class PlanSerializer(serializers.ModelSerializer, CommonFields):
    type = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    point = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    participation_active = serializers.SerializerMethodField()
    participation_string = serializers.SerializerMethodField()
    published_projects_count = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ['type', 'title', 'url',
                  'organisation', 'point',
                  'point_label', 'cost',
                  'district', 'topic', 'status',
                  'status_display',
                  'participation',
                  'participation_string',
                  'participation_active',
                  'published_projects_count']

    def _get_status_string(self, projects):
        future_phase = None
        for project in projects:
            phases = project.phases
            if phases.active_phases():
                return _('running')
            if phases.future_phases() and \
               phases.future_phases().first().start_date:
                date = phases.future_phases().first().start_date
                if not future_phase:
                    future_phase = date
                else:
                    if date < future_phase:
                        future_phase = date

        if future_phase:
            return _('starts at {}').format(future_phase.date())

    def _get_participation_status_plan(self, item):
        projects = item.projects.all() \
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

    def get_type(self, instance):
        return 'plan'

    def get_url(self, instance):
        return instance.get_absolute_url()

    def get_status_display(self, instance):
        return instance.get_status_display()

    def get_published_projects_count(self, instance):
        return instance.published_projects.count()

    def get_participation_string(self, instance):
        participation_string, active = \
            self._get_participation_status_plan(instance)
        return str(participation_string)

    def get_participation_active(self, instance):
        participation_string, active = \
            self._get_participation_status_plan(instance)
        return active
