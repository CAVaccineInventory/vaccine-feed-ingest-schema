import enum

import pydantic.error_wrappers
import pytest
from vaccine_feed_ingest_schema import location

from .common import collect_existing_subclasses


def test_has_expected_schema():
    expected = {
        "BaseModel",
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
    }

    existing = collect_existing_subclasses(location, pydantic.BaseModel)

    missing = expected - existing
    assert not missing, "Expected pydantic schemas are missing"

    extra = existing - expected
    assert not extra, "Extra pydantic schemas found. Update this test."


def test_has_expected_enums():
    expected = {
        "State",
        "ContactType",
        "DayOfWeek",
        "LocationAuthority",
        "VaccineProvider",
        "VaccineSupply",
        "VaccineType",
        "WheelchairAccessLevel",
    }

    existing = collect_existing_subclasses(location, enum.Enum)

    missing = expected - existing
    assert not missing, "Expected enums are missing"

    extra = existing - expected
    assert not extra, "Extra enum found. Update this test."


def test_valid_contact():
    assert location.Contact(
        contact_type=location.ContactType.BOOKING,
        email="vaccine@example.com",
    )
    assert location.Contact(website="https://example.com")
    assert location.Contact(phone="(510) 555-5555")


def test_raises_on_invalid_contact():
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        location.Contact(contact_type=location.ContactType.GENERAL)

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        location.Contact(contact_type="invalid", email="vaccine@example.com")

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        location.Contact(email="vaccine@example.com", website="https://example.com")


def test_raises_on_invalid_location():
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        location.NormalizedLocation()

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        location.NormalizedLocation(
            id="source:id",
            contact=location.Contact(phone="444-444"),
            source=location.Source(
                source="source",
                id="id",
                data={"id": "id"},
            ),
        )

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        location.NormalizedLocation(
            id="invalid:id",
            source=location.Source(
                source="source",
                id="id",
                data={"id": "id"},
            ),
        )


def test_valid_location():
    # Minimal record
    assert location.NormalizedLocation(
        id="source:id",
        source=location.Source(
            source="source",
            id="id",
            data={"id": "id"},
        ),
    )

    # Full record with str enums
    assert location.NormalizedLocation(
        id="source:id",
        name="name",
        address=location.Address(
            street1="1991 Mountain Boulevard",
            street2="#1",
            city="Oakland",
            state="CA",
            zip="94611",
        ),
        location=location.LatLng(
            latitude=37.8273167,
            longitude=-122.2105179,
        ),
        contact=[
            location.Contact(
                contact_type="booking",
                phone="(916) 445-2841",
            )
        ],
        languages=["en"],
        opening_dates=[
            location.OpenDate(
                opens="2021-04-01",
                closes="2021-04-01",
            ),
        ],
        opening_hours=[
            location.OpenHour(
                day="monday",
                opens="08:00",
                closes="14:00",
            ),
        ],
        availability=location.Availability(
            drop_in=False,
            appointments=True,
        ),
        inventory=[
            location.Vaccine(
                vaccine="moderna",
                supply_level="in_stock",
            ),
        ],
        access=location.Access(
            walk=True,
            drive=False,
            wheelchair="partial",
        ),
        parent_organization=location.Organization(
            id="rite_aid",
            name="Rite Aid",
        ),
        links=[
            location.Link(
                authority="google_places",
                id="abc123",
            ),
        ],
        notes=["note"],
        active=True,
        source=location.Source(
            source="source",
            id="id",
            data={"id": "id"},
        ),
    )
