import pydantic
import pytest

from vaccine_feed_ingest_schema import location

VALID_AUTHORITIES = [
    "wa_argcis",
    "vaccinespotter_org",
    "some_randmom_entity_of_sorts",
    "ma",
    "ma123"
]

INVALID_AUTHORITIES = [
    "wa:argcis",
    "wa/arcgiz",
    "@vaccinespotter",
    "SomeRandomEntity",
    "MA"
]


@pytest.mark.parametrize("valid_authority", VALID_AUTHORITIES)
def test_valid_authority(valid_authority):
    assert location.Link(authority=valid_authority, id="abc123")


@pytest.mark.parametrize("invalid_authority", INVALID_AUTHORITIES)
def test_invalid_authority(invalid_authority):
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        location.Link(authority=invalid_authority, id="abc123")


VALID_LOCATION_IDS = ["{}:abc123".format(a) for a in VALID_AUTHORITIES]

INVALID_LOCATION_IDS = ["{}:abc123".format(a) for a in INVALID_AUTHORITIES] + [
    "cvs123", # no colon
    "wa:arcgis:abc123" # two colons
]


@pytest.mark.parametrize("valid_id", VALID_LOCATION_IDS)
def test_valid_location_id(valid_id):
    source, id = valid_id.split(":")

    assert location.NormalizedLocation(id=valid_id, source=location.Source(source=source, id=id, data={}))


@pytest.mark.parametrize("invalid_id", INVALID_LOCATION_IDS)
def test_invalid_location_id(invalid_id):
    parts = invalid_id.split(":")
    if len(parts) == 2:
        source, id = parts
    else:
        source = "test_source"
        id = invalid_id

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        location.NormalizedLocation(id=invalid_id, source=location.Source(source=source, id=id, data={}))

