import inspect
from importlib import reload

import pydantic.error_wrappers
import pytest

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

    class_tuples = inspect.getmembers(schema, inspect.isclass)
    classes = list(map(lambda class_tuple: class_tuple[0], class_tuples))

    expected_classes = [
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
    ]

    for expected_class in expected_classes:
        if expected_class not in classes:
            raise KeyError(f"Expected class {expected_class} is not defined.")

    for klass in classes:
        if klass not in expected_classes:
            raise KeyError(f"Extra class {klass} defined. Did you update your tests?")


@pytest.mark.filterwarnings(f"ignore: {DEPRECATION_SNIPPET}")
def test_raises_on_invalid_location():
    from vaccine_feed_ingest_schema import schema

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        schema.NormalizedLocation()
