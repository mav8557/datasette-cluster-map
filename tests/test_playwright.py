import pytest

try:
    from playwright import sync_api
except ImportError:
    sync_api = None
import pytest
import nest_asyncio
from urllib.parse import parse_qs, urlparse

nest_asyncio.apply()

pytestmark = pytest.mark.skipif(sync_api is None, reason="playwright not installed")


def test_map_does_not_request_next_url(ds_server, page):
    # Datasette 1.x returns a 400 error if _extra=next_url is requested
    with page.expect_request(lambda request: "_shape=objects" in request.url) as info:
        page.goto(ds_server + "/data/lat_lng")
    assert parse_qs(urlparse(info.value.url).query)["_extra"] == ["count"]
    sync_api.expect(page.locator(".leaflet-marker-icon")).to_have_count(2)


@pytest.mark.parametrize(
    "table",
    (
        "foo_latitude_foo_longitude",
        "lat_lng",
        "lat_lon",
        "lat_long",
        "latitude_longitude",
    ),
)
def test_markers_are_displayed(ds_server, table, page):
    page.goto(ds_server + "/data/" + table)
    # There should be two leaflet-marker-icons
    sync_api.expect(page.locator(".leaflet-marker-icon")).to_have_count(2)
