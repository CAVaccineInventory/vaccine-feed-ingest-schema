import pydantic
from vaccine_feed_ingest_schema import load

from .common import collect_existing_subclasses


def test_has_expected_schema():
    expected = {
        "BaseModel",
        "NormalizedLocation",
        "ImportMatchAction",
        "ImportSourceLocation",
    }

    existing = collect_existing_subclasses(load, pydantic.BaseModel)

    missing = expected - existing
    assert not missing, "Expected pydantic schemas are missing"

    extra = existing - expected
    assert not extra, "Extra pydantic schemas found. Update this test."
