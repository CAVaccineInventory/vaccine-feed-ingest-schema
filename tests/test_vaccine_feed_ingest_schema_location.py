import inspect

import pydantic.error_wrappers
import pytest

from vaccine_feed_ingest_schema import location


def test_has_expected_classes():
    class_tuples = inspect.getmembers(location, inspect.isclass)
    classes = list(map(lambda class_tuple: class_tuple[0], class_tuples))

    expected_classes = [
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
    ]

    for expected_class in expected_classes:
        if expected_class not in classes:
            raise KeyError(f"Expected class {expected_class} is not defined.")

    for klass in classes:
        if klass not in expected_classes:
            raise KeyError(f"Extra class {klass} defined. Did you update your tests?")


def test_raises_on_invalid_location():
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        location.NormalizedLocation()
