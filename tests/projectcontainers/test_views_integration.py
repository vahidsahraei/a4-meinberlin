import pytest

from tests.helpers import assert_template_response


@pytest.mark.django_db
def test_detail_view(client, project_container):
    url = project_container.get_absolute_url()
    response = client.get(url)
    assert_template_response(
        response, 'a4projects/project_detail.html')

    assert 'meinberlin_projectcontainers/includes/container_detail.html' \
        in (template.name for template in response.templates)
