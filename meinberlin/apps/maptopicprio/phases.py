from django.utils.translation import ugettext_lazy as _

from adhocracy4 import phases

from . import apps
from . import models
from . import views


class MapPrioritizePhase(phases.PhaseContent):
    app = apps.Config.label
    phase = 'prioritize'
    weight = 20
    view = views.MapTopicListView

    name = _('Prioritize phase')
    description = _('Prioritize and comment topics located on a map.')
    module_name = _('spatial topic prioritization')

    features = {
        'comment': (models.MapTopic,),
        'rate': (models.MapTopic,),
    }


phases.content.register(MapPrioritizePhase())
