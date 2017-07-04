from pytest_factoryboy import register

from tests.exports import factories
from tests.ideas import factories as ideas_factories

register(ideas_factories.IdeaFactory)
register(factories.RatingFactory)
register(factories.ModeratorStatementFactory)
register(factories.ProposalFactory)
