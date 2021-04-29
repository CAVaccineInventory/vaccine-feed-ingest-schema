from importlib import reload

import pydantic.error_wrappers
import pytest

from .common import collect_existing_subclasses

DEPRECATION_SNIPPET = "vaccine_feed_ingest_schema.schema is deprecated."


def test_warn_on_import():
    with pytest.warns(DeprecationWarning, match=DEPRECATION_SNIPPET):
        from vaccine_feed_ingest_schema import schema

        # Depending on the order in which tests run, the above import may be
        # skipped. Reload it so that we trigger the warning, if it exists.
        reload(schema)


@pytest.mark.filterwarnings(f"ignore: {DEPRECATION_SNIPPET}")
def test_has_expected_classes():
    from vaccine_feed_ingest_schema import schema

    expected = {
        "Address",
        "LatLng",
        "Contact",
        "OpenDate",
        "OpenHour",
        "Availability",
        "Vaccine",
        "Access",
        "Organization",
        "Link",
        "Source",
        "NormalizedLocation",
        "ImportMatchAction",
        "ImportSourceLocation",
    }

    existing = collect_existing_subclasses(schema, pydantic.BaseModel)

    missing = expected - existing
    assert not missing, "Expected pydantic schemas are missing"

    extra = existing - expected
    assert not extra, "Extra pydantic schemas found. Update this test."


@pytest.mark.filterwarnings(f"ignore: {DEPRECATION_SNIPPET}")
def test_raises_on_invalid_location():
    from vaccine_feed_ingest_schema import schema

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        schema.NormalizedLocation()
