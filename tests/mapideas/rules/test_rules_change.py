import pytest
import rules

from meinberlin.apps.mapideas import phases
from meinberlin.test.helpers import freeze_phase
from meinberlin.test.helpers import freeze_post_phase
from meinberlin.test.helpers import freeze_pre_phase
from meinberlin.test.helpers import setup_phase
from meinberlin.test.helpers import setup_users

perm_name = 'meinberlin_mapideas.change_mapidea'


def test_perm_exists():
    assert rules.perm_exists(perm_name)


@pytest.mark.django_db
def test_pre_phase(phase_factory, map_idea_factory, user):
    phase, _, project, item = setup_phase(phase_factory, map_idea_factory,
                                          phases.CollectPhase)
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator

    assert project.is_public
    with freeze_pre_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert not rules.has_perm(perm_name, creator, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_phase_active(phase_factory, map_idea_factory, user):
    phase, _, project, item = setup_phase(phase_factory, map_idea_factory,
                                          phases.CollectPhase)
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator

    assert project.is_public
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert rules.has_perm(perm_name, creator, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_phase_active_project_draft(phase_factory, map_idea_factory, user):
    phase, _, project, item = setup_phase(phase_factory, map_idea_factory,
                                          phases.CollectPhase,
                                          module__project__is_draft=True)
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator

    assert project.is_draft
    with freeze_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert not rules.has_perm(perm_name, creator, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)


@pytest.mark.django_db
def test_post_phase_project_archived(phase_factory, map_idea_factory, user):
    phase, _, project, item = setup_phase(phase_factory, map_idea_factory,
                                          phases.CollectPhase,
                                          module__project__is_archived=True)
    anonymous, moderator, initiator = setup_users(project)
    creator = item.creator

    assert project.is_archived
    with freeze_post_phase(phase):
        assert not rules.has_perm(perm_name, anonymous, item)
        assert not rules.has_perm(perm_name, user, item)
        assert not rules.has_perm(perm_name, creator, item)
        assert rules.has_perm(perm_name, moderator, item)
        assert rules.has_perm(perm_name, initiator, item)
